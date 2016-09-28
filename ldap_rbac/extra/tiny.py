# -*- coding: utf-8 -*-
from resources import Resource, ResourceHelper
from acls import AccessControlList, AccessControlListHelper
from tags import TagsHelper
from logger import ResourceLogger
from tinydb import Query


class TinyDbAccessControlList(AccessControlListHelper):
    def __init__(self, db=None, table=None):
        self.db = db
        self.table=table

    def load(self, resource, force=False):
        pass

    def add(self, resource, aces, user=None):
        pass

    def remove(self, resource, aces, user=None):
        pass

    def clear(self, resource):
        pass

    def save(self, resource):
        pass


class TinyDbTags(TagsHelper):
    def __init__(self, db=None, table=None):
        self.db = db
        self.table = table

    def load(self, resource, force=False):
        pass

    def add(self, resource, tags, user=None):
        pass

    def remove(self, resource, tags, user=None):
        pass

    def clear(self, resource):
        pass

    def save(self, resource):
        pass


class TinyDbLogger(ResourceLogger):
    def __init__(self, db=None, table=None):
        self.db = db
        self.table = table

    def log(self, resource, event=None, user=None, **kwargs):
        pass


class TinyDbResources(ResourceHelper):
    def __init__(self, root=None, acls=None, tags=None, logger=None,
                 db=None, enable_acl=True, enable_tags=True, enable_log=True,
                 enable_access_log=True, enable_operation_log=False):
        self.db = db
        if enable_acl and acls is None:
            acls = TinyDbAccessControlList(db=db)
        if enable_tags and tags is None:
            acls = TinyDbTags(db=db)
        if enable_log and logger is None:
            acls = TinyDbLogger(db=db)
        super(TinyDbResources, self).__init__(
            root=root,
            acls=acls, tags=tags, logger=logger,
            enable_access_log=enable_access_log, enable_operation_log=enable_operation_log)

    def is_acl_together(self):
        return self.is_acl_support and isinstance(self.acls, TinyDbAccessControlList) \
               and self.acls.db == self.db and self.acls.table is None

    def is_tag_together(self):
        return self.is_tag_support and isinstance(self.tags, TinyDbTags) \
               and self.tags.db == self.db and self.tags.table is None

    def query_of_user(self, user=None):
        pass

    def query(self, dsl):
        pass

    def create(self, resource, user=None, **kwargs):
        pass

    def load(self, resource, result):
        changes = []
        if resource.rid is None:
            resource.rid = result.get('rid')
        elif resource.rid != result.get('rid'):
            changes.append('rid')
        if resource.owner is None:
            resource.owner = result.get('owner')
        elif resource.owner != result.get('owner'):
            changes.append('owner')
        if resource.group is None:
            resource.group = result.get('group')
        elif resource.group != result.get('group'):
            changes.append('group')
        # if resource.rid is None:
        #    resource.children = result.get('children')
        # elif resource.rid != result.get('rid'):
        #    changes.append('rid')
        if resource.mode is None:
            resource.mode = result.get('mode')
        elif resource.mode != result.get('mode'):
            changes.append('mode')
        if resource.ctime is None:
            resource.ctime = result.get('ctime')
        elif resource.ctime != result.get('ctime'):
            changes.append('ctime')
        if resource.mtime is None:
            resource.mtime = result.get('mtime')
        elif resource.mtime != result.get('mtime'):
            changes.append('mtime')
        if resource.atime is None:
            resource.atime = result.get('atime')
        elif resource.atime != result.get('atime'):
            changes.append('atime')
        if resource.links is None:
            resource.links = result.get('links')
        elif resource.links != result.get('links'):
            changes.append('links')
        if resource.blocks is None:
            resource.blocks = result.get('blocks')
        elif resource.blocks != result.get('blocks'):
            changes.append('blocks')
        if resource.loaded_xattrs is None:
            resource.loaded_xattrs = result.get('xattrs')
        elif resource.loaded_xattrs != result.get('xattrs'):
            changes.append('xattrs')
        if self.is_acl_together():
            resource.loaded_acls = AccessControlList(ace_text_list=result.get('acls'))
        if self.is_tag_together():
            resource.loaded_tags = None
        resource.loaded = True
        return resource, changes

    def find_by_path(self, path, **kwargs):
        if not path.startswith(self.root.path):
            return None
        rel_path = self.rel_path(path)
        if len(rel_path) == 0:
            return self.root
        query = Query()
        result = self.db.get(query.path == rel_path)
        if result is None:
            return result
        resource = self.instance_by_path(rel_path)
        self.load(resource, result)

    def find_by_id(self, rid, **kwargs):
        pass

    def find_all(self, query, **kwargs):
        pass

    def count(self, query, **kwargs):
        pass

    def update(self, resource, user=None, **kwargs):
        pass

    def delete(self, path, user=None, **kwargs):
        pass

    def update_xattrs(self, resource, xattrs):
        pass

    def load_xattrs(self, resource):
        pass

    def clear_xattrs(self, resource):
        pass

    def remove_xattrs(self, resource, keys):
        pass