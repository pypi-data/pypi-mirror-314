from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import func, update
from sqlalchemy.exc import SQLAlchemyError
from .models import SuperTab
from sqlalchemy import cast, JSON


class TabManager:
    def __init__(self, engine, retain_child_tab=0, tab_info_parent_mapping_key=None, tab_info_child_key_for_parent_mapping=None, current_tab_closing_movement_direction = 'RIGHT'):
        
        self.retain_child_tab = retain_child_tab
        self.tab_info_parent_mapping_key = tab_info_parent_mapping_key
        self.tab_info_child_key_for_parent_mapping = tab_info_child_key_for_parent_mapping
        self.current_tab_closing_movement_direction = current_tab_closing_movement_direction

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    def _get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def open_tab(self, unique_identifier, created_by, tab_info, parent_tab_id=None, tab_id = None):
        session = self.SessionLocal()
        try:
            # Validate parent tab if parent_tab_id is provided
            if parent_tab_id:
                parent_tab = session.query(SuperTab).filter_by(id=parent_tab_id).first()
                if not parent_tab:
                    raise ValueError("Parent tab not found")
                level = parent_tab.level + 1
                max_order = session.query(func.max(SuperTab.order)).filter_by(
                    unique_identifier=unique_identifier,
                    level=level,
                    parent_tab_id=parent_tab_id
                ).scalar() or 0
                if max_order > 99 : 
                    raise ValueError("Max tabs opened is 100")
            else:
                q = session.query(SuperTab.id).filter_by(unique_identifier=unique_identifier, level = 0).scalar()
                if q : 
                    if q != tab_id : 
                        raise ValueError("Can only have 1 level 0, please add parent_tab_id")
                level = 0
                max_order = 0
                parent_tab_id = 0

            # Update previous current tab to not current
            session.query(SuperTab).filter_by(unique_identifier=unique_identifier, is_current_tab=True).update({"is_current_tab": False})
            
            #update current tab if already opened
            parent_tab_order = None
            if tab_id : 
                #check if tab is in dropdown or visibile header
                tab_to_open = session.query(SuperTab).filter(SuperTab.id==tab_id).first()
                if tab_to_open.order == 0 and tab_to_open.level != 0 : 
                    #tab is in dropdown so we need to reorder tabs
                    #self.reorder_tabs(tab_id, 1)
                    tab_to_put_in_list = session.query(SuperTab).filter(SuperTab.parent_tab_id == tab_to_open.parent_tab_id, SuperTab.order != 0).order_by(SuperTab.last_opened).first()
                    session.query(SuperTab).filter(SuperTab.parent_tab_id == tab_to_open.parent_tab_id, SuperTab.order > tab_to_put_in_list.order).update({"order" : SuperTab.order - 1}, synchronize_session=False)
                    session.query(SuperTab).filter(SuperTab.id == tab_to_put_in_list.id).update({"order" : 0})
                    session.query(SuperTab).filter(SuperTab.id==tab_id).update({"tab_info" : tab_info, "is_current_tab": True, "last_opened" :func.now(), "order" : 9 }, synchronize_session=False)
                    session.commit()
                    parent_tab_order = session.query(SuperTab.id , SuperTab.order).filter(SuperTab.parent_tab_id == tab_to_open.parent_tab_id, SuperTab.order != 0).all()
                else : 
                    # open visible tab
                    session.query(SuperTab).filter(SuperTab.id==tab_id).update({"tab_info":  tab_info, "is_current_tab": True, "last_opened" :func.now()}, synchronize_session=False)
                new_tab = session.query(SuperTab).filter(SuperTab.id == tab_id).first()
            
            # Add new tab
            else :
                if max_order == 9 :
                    tab_to_put_in_list = session.query(SuperTab).filter(SuperTab.parent_tab_id == parent_tab_id, SuperTab.order != 0).order_by(SuperTab.last_opened).first()
                    session.query(SuperTab).filter(SuperTab.parent_tab_id == parent_tab_id, SuperTab.order > tab_to_put_in_list.order).update({"order" : SuperTab.order - 1}, synchronize_session=False)
                    session.query(SuperTab).filter(SuperTab.id == tab_to_put_in_list.id).update({"order" : 0})
                    session.commit()
                    parent_tab_order = session.query(SuperTab.id , SuperTab.order).filter(SuperTab.parent_tab_id == parent_tab_id, SuperTab.order != 0).all()
                    tab_new_order = 9
                else : 
                    tab_new_order = max_order + 1

                new_tab = SuperTab(
                    created_by=created_by,
                    unique_identifier=unique_identifier,
                    level=level,
                    is_current_tab=True,
                    tab_info=tab_info,
                    parent_tab_id=parent_tab_id,
                    order=tab_new_order if parent_tab_id else 0,
                    last_opened=func.now()
                )
            session.add(new_tab)
            session.commit()
                            
            output = new_tab.to_dict()
            if parent_tab_order : 
                output['parent_tab_order'] = parent_tab_order

            # Find orphaned children

            if self.retain_child_tab == 1 and self.tab_info_child_key_for_parent_mapping:
                orphaned_children = session.query(SuperTab).filter(
                    SuperTab.unique_identifier == unique_identifier,
                    SuperTab.parent_tab_id == None,
                    func.json_extract(SuperTab.tab_info, '$.' + self.tab_info_child_key_for_parent_mapping) == tab_info[self.tab_info_parent_mapping_key]
                ).all()
                
                print("Orphaned children found:", [child.id for child in orphaned_children])
                children = []
                #update({'parent_tab_id' : new_tab.id}, synchronize_session = False)

                for child in orphaned_children:
                    child.parent_tab_id = new_tab.id
                    session.add(child)
                    children.append(child.to_dict())
                session.commit()
                if len(children) > 0 :
                    output['children'] = children
            return output

        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally :
            session.close()

    def close_tab(self, tab_id):
        session = self.SessionLocal()
        if 1==1 : 
        #try:
            tab_to_close = session.query(SuperTab).filter_by(id=tab_id).first()
            if not tab_to_close:
                raise ValueError("Tab not found")
            
            tab_order = tab_to_close.order
            tab_unique_id = tab_to_close.unique_identifier
            tab_level = tab_to_close.level
            tab_parent_id = tab_to_close.parent_tab_id
            is_current_tab = tab_to_close.is_current_tab

            session.delete(tab_to_close)
            child_current_tab = session.query(func.max(SuperTab.is_current_tab)).filter_by(parent_tab_id=tab_id).scalar()
            max_order = session.query(func.max(SuperTab.order)).filter(SuperTab.parent_tab_id == tab_parent_id).scalar()
            if self.retain_child_tab == 0 : 
                child_tab_to_close = session.query(SuperTab).filter_by(parent_tab_id=tab_id).delete()
            else :
                # make them orphans by setting parent_tab_id = 0 
                child_tab_to_close = session.query(SuperTab).filter_by(parent_tab_id=tab_id).update({"parent_tab_id": None, "is_current_tab": 0})

            session.commit()
            # Adjust the order of remaining tabs
            if tab_order != 0 : 
                session.query(SuperTab).filter(
                    SuperTab.unique_identifier == tab_unique_id,
                    SuperTab.level == tab_level,
                    SuperTab.parent_tab_id == tab_parent_id,
                    SuperTab.order > tab_order
                ).update({"order": SuperTab.order - 1}, synchronize_session=False)

            if is_current_tab == 1 or child_current_tab == 1: 
                if self.current_tab_closing_movement_direction == 'PARENT' : 
                    session.query(SuperTab).filter(SuperTab.id == tab_parent_id).update({"is_current_tab" : True})
                elif self.current_tab_closing_movement_direction == 'RIGHT' : 
                    if max_order > tab_order :  
                        session.query(SuperTab).filter(SuperTab.parent_tab_id == tab_parent_id, SuperTab.order == tab_order).update({"is_current_tab" : True})
                    elif max_order == tab_order : 
                        if int(tab_order) != 1  :
                            session.query(SuperTab).filter(SuperTab.parent_tab_id == tab_parent_id, SuperTab.order == tab_order -1).update({"is_current_tab" : True})
                        else : # this is for case only one id was open 
                            session.query(SuperTab).filter(SuperTab.id == tab_parent_id).update({"is_current_tab" : True})
                    

            session.commit()

            current_tab_id = session.query(SuperTab.id).filter(SuperTab.unique_identifier == tab_unique_id, SuperTab.is_current_tab == 1).scalar()

            #check if there are any subtabs in the list whose space has opened up
            tab_to_get_out_of_list  = session.query(SuperTab).filter(SuperTab.parent_tab_id == tab_parent_id, SuperTab.order == 0 ).order_by(SuperTab.last_opened.desc()).first()
            if tab_to_get_out_of_list : 
                session.query(SuperTab).filter(SuperTab.id == tab_to_get_out_of_list.id).update({"order":9})
                session.commit()
            session.close()
            return current_tab_id

    def reorder_tabs(self, tab_id, new_order):
        session = self.SessionLocal()
        try:
            tab_to_reorder = session.query(SuperTab).filter_by(id=tab_id).first()
            if not tab_to_reorder:
                raise ValueError("Tab not found")
            
            old_order = tab_to_reorder.order
            unique_identifier = tab_to_reorder.unique_identifier
            level = tab_to_reorder.level
            parent_tab_id = tab_to_reorder.parent_tab_id

            # Get the maximum order
            max_order = session.query(func.max(SuperTab.order)).filter_by(
                unique_identifier=unique_identifier,
                level=level,
                parent_tab_id=parent_tab_id
            ).scalar()

            # Check if new_order is greater than max_order + 1
            if new_order > max_order + 1:
                raise ValueError("New order exceeds the maximum allowed order")
        
            if new_order > old_order:
                # Temporarily set tab order to 0
                tab_to_reorder.order = 0
                session.commit()

                # Update orders of other tabs
                session.query(SuperTab).filter(
                    SuperTab.unique_identifier == unique_identifier,
                    SuperTab.level == level,
                    SuperTab.parent_tab_id == parent_tab_id,
                    SuperTab.order.between(old_order, new_order)
                ).update({"order": SuperTab.order - 1}, synchronize_session=False)
                session.commit()

                tab_to_reorder.order = new_order
                session.commit()
            elif new_order < old_order:
                # Temporarily set tab order to 0
                tab_to_reorder.order = 0
                session.commit()

                # Update orders of other tabs
                session.query(SuperTab).filter(
                    SuperTab.unique_identifier == unique_identifier,
                    SuperTab.level == level,
                    SuperTab.parent_tab_id == parent_tab_id,
                    SuperTab.order.between(new_order, old_order)
                ).update({"order": SuperTab.order + 1}, synchronize_session=False)

                session.commit()
                tab_to_reorder.order = new_order
                session.commit()
            

            # allow only 9 open sub tabs
            session.query(SuperTab).filter(
                    SuperTab.unique_identifier == unique_identifier,
                    SuperTab.level == level,
                    SuperTab.parent_tab_id == parent_tab_id,
                    SuperTab.order > 9
                    ).update({"order":0} , synchronize_session=False)
            session.commit()
            
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally :
            session.close()

    def get_tab(self, unique_identifier, parent_tab_id=None, level=None):
        session = self.SessionLocal()
        try:
            query = session.query(SuperTab).filter_by(unique_identifier=unique_identifier)

            if self.retain_child_tab == 1: 
                query = query.filter(SuperTab.parent_tab_id!=None)
            if parent_tab_id is not None:
                query = query.filter_by(parent_tab_id=parent_tab_id)
            if level is not None:
                query = query.filter_by(level=level)
            tabs = query.order_by(SuperTab.last_opened.desc()).all()

            if not tabs : 
                raise ValueError ("No tabs")
            current_tab = session.query(SuperTab).filter_by(unique_identifier=unique_identifier, is_current_tab=True).first()
            return {
                "tabs": [tab.to_dict() for tab in tabs],
                "current_tab": current_tab.to_dict()
            }
        except SQLAlchemyError as e:
            raise e
        finally :
            session.close()

    def get_identifiers_with_prefix(self, prefix):
        
        session = self.SessionLocal()
        try:
            identifiers = session.query(SuperTab.unique_identifier).filter(
                SuperTab.unique_identifier.like(f"{prefix}%")
            ).distinct().all()
            return [identifier[0] for identifier in identifiers]
        except SQLAlchemyError as e:
            raise e
        finally :
            session.close()

    def copy_tabs(self, from_unique_identifier, to_unique_identifier):
        session = self.SessionLocal()
        try:
            # Delete existing tabs for the new identifier
            session.query(SuperTab).filter_by(unique_identifier=to_unique_identifier).delete()
            session.flush()

            # Get all tabs for the from_unique_identifier
            tabs_to_copy = session.query(SuperTab).filter_by(unique_identifier=from_unique_identifier).all()
            new_tabs = []
            for tab in tabs_to_copy:
                new_tab = SuperTab(
                    created_by=tab.created_by,
                    unique_identifier=to_unique_identifier,
                    level=tab.level,
                    is_current_tab=tab.is_current_tab,
                    tab_info=tab.tab_info,
                    parent_tab_id=tab.parent_tab_id,
                    order=tab.order,
                    last_opened=tab.last_opened
                )
                new_tabs.append(new_tab)
            session.bulk_save_objects(new_tabs)
            session.commit()

            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally :
            session.close()


# Usage Example
#uif __name__ == "__main__":
#    tab_manager = TabManager()
#    unique_identifier = "user12345"
#    created_by = 1
#
#    # Open a new tab
#    new_tab = tab_manager.open_tab(unique_identifier, created_by, {"info": "test"}, parent_tab_id=None)
#    print(f"New tab opened: {new_tab}")
#
#    # Close a tab
#    try:
#        success = tab_manager.close_tab(new_tab.id)
#        print(f"Tab closed: {success}")
#    except ValueError as e:
#        print(e)
#
#    # Reorder tabs
#    try:
#        success = tab_manager.reorder_tabs(new_tab.id, new_order=2)
#        print(f"Tabs reordered: {success}")
#    except ValueError as e:
#        print(e)
#
#    # Get current tab
#    tab_info = tab_manager.get_tab(unique_identifier)
#    print(f"Tab info: {tab_info}")
