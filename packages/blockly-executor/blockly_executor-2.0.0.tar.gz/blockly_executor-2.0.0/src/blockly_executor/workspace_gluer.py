from blockly_executor import ExtException
from .workspace import Workspace


class WorkspaceGluer:
    workspace = Workspace

    @classmethod
    def unglue(cls, base: Workspace, custom: Workspace):
        changes = []
        errors = []
        warnings = []

        custom_index = custom.create_index_of_block()
        base_index = base.create_index_of_block()
        custom_new = list(custom_index.keys())
        # base_not_ready = list(base_index.keys())
        for block_id in base_index:
            base_block = base_index[block_id]
            custom_block = custom_index.get(block_id)
            compare_result = None
            if custom_block:
                compare_result = cls.compare_block(custom, base, block_id, custom_block, base_block, errors, warnings)
            else:
                changes.append(dict(
                    id=block_id,
                    type=base_block.get('type'),
                    delete=True,
                    parent=base_block.get('parent'),
                    previous=base_block.get('previous'),
                    next=base_block.get('next')
                ))
            if compare_result:
                changes.append(compare_result)
            # base_not_ready.pop(block_id)
            if custom_block:
                custom_new.remove(block_id)
        new_blocks = []
        for block_id in custom_new:
            # блоки которых нет в базовом
            custom_block = custom_index[block_id]
            new_blocks.append(dict(
                id=block_id,
                type=custom_block.get('type'),
                new=True,
                parent=custom_block.get('parent'),
                previous=custom_block.get('previous'),
                next=custom_block.get('next')
            ))
        return new_blocks + changes, errors, warnings

    @classmethod
    def glue(cls, base: Workspace, custom: Workspace, changes: list = None):
        def move_block(_block, append_to_root=False):
            _parent = change.get('parent')
            _previous = change.get('previous')
            _parent_block = None  # todo root
            if _parent:
                _parent_block = base_index.get(_parent[1])
            elif _previous:
                _parent = ('next', _previous)
                _parent_block = base_index.get(_previous)
            if _parent and _parent[0] and _parent[1]:
                cls.workspace.set_input(_parent_block['node'], _parent[0], _block['node'])
                _parent_block['inputs'][_parent[0]] = _block['node'].get('id')
            elif append_to_root:
                base.root_append_block(_block['node'])
        try:
            if changes is None:
                gluer_result = custom.gluer_result_read()
                changes = gluer_result.get('changes', [])

            errors = []
            warnings = []

            custom_index = custom.create_index_of_block()
            base_index = base.create_index_of_block()
            for change in changes:
                block_id = change['id']
                block_changed = change.get('changed')
                base_block = base_index.get(block_id)
                custom_block = custom_index.get(block_id)
                is_new_block = change.get('new')

                if change.get('delete'):
                    parent = base_block.get('parent')
                    parent_block = base_index.get(parent[1])
                    if parent:
                        if parent_block:
                            if parent_block['inputs'][parent[0]] == block_id:
                                cls.workspace.set_input(parent_block['node'], parent[0], None)
                            else:
                                pass  # если в инпуте уже другой блок, то делать ничего не надо
                        else:
                            raise NotImplementedError()
                    else:
                        base.root_delete_block(parent[0])

                    continue

                if is_new_block:
                    move_block(custom_block, True)
                    base_index[block_id] = custom_block
                    pass
                    # new_parent_block = base_index.get(change_parent)

                if block_changed:
                    if base_block:
                        move_block(base_block, False)

                        items = change.get('delete_inputs', [])
                        for item_name in items:
                            cls.workspace.delete_input(base_block['node'], item_name)

                        items = change.get('new_fields', [])
                        for item_name in items:
                            field_value = cls.workspace.find_field_by_name(custom_block['node'], item_name)
                            cls.workspace.set_field_value(base_block['node'], item_name, field_value)

                        items = change.get('delete_fields', [])
                        for item_name in items:
                            cls.workspace.delete_field(custom_block['node'], item_name)
                            pass

                        items = change.get('change_fields', {})
                        for item_name in items:
                            field_value = items[item_name][0]
                            cls.workspace.set_field_value(base_block['node'], item_name, field_value)

                        items = change.get('change_mutations', {})
                        for item_name in items:
                            mutation_value = items[item_name][0]
                            cls.workspace.set_mutation_value(base_block['node'], item_name, mutation_value)
                        pass
                    else:
                        if block_changed:
                            if base_block:
                                pass
                            else:
                                pass
                change_parent = change.get('parent')
                if not block_changed and change_parent is not None:
                    new_parent_block = base_index.get(change_parent[1])
                    if new_parent_block:
                        cls.workspace.set_input(new_parent_block['node'], change_parent[0], custom_block['node'])
                        # base_index[]
                        pass
                    else:
                        pass

                # elif change.get('move'):
                #     if base_block:
                #         parent_block = base_index.get(base_block[link_name])
                #         if parent_block:
                #             pass
                #         else:
                #             pass
                #     else:
                #         pass
                # if change.get('new'):
                #     if base_block:
                #         pass
                #     else:
                #         pass
                # base.gluer_result_update(base.own, changes, errors, warnings)
            return base.get_raw(), changes, errors, warnings
        except Exception as err:
            raise ExtException(parent=err) from err

    @classmethod
    def compare_block(cls, custom, base, block_id, custom_block, base_block, errors: list, warnings: list) -> dict:
        result = dict(
            # move=False,
            # new=False,
            # change_fields={},
            # delete=False
            # change_inputs={},
            # change_next=False
        )

        if base_block['type'] != custom_block['type']:
            errors.append(
                dict(message='Изменен тип блока', detail=f"{block_id} {base_block['type']} {custom_block['type']}"))
            result['type'] = custom_block['type']

        cls.compare_link('parent', result, block_id, custom_block, base_block, errors, warnings)
        # cls.compare_link('next', result, block_id, custom_block, base_block, errors, warnings)
        cls.compare_link('previous', result, block_id, custom_block, base_block, errors, warnings)
        cls.compare_inputs(result, block_id, custom_block, base_block, errors, warnings)
        cls.compare_fields(custom, base, result, block_id, custom_block, base_block, errors, warnings)
        cls.compare_mutations(result, block_id, custom_block, base_block, errors, warnings)
        if result:
            result['id'] = block_id
            result['type'] = custom_block['type']
        return result

    @classmethod
    def compare_inputs(cls, result, block_id, custom_block, base_block, errors: list, warnings: list):
        for input_name in base_block['inputs']:
            if input_name in custom_block['inputs']:
                custom_input = custom_block['inputs'].pop(input_name, None)
                if base_block['inputs'][input_name] != custom_input:
                    try:
                        result['change_inputs']
                    except KeyError:
                        result['change_inputs'] = {}
                    result['change_inputs'][input_name] = custom_input
                    # result['changed'] = True
            else:
                try:
                    result['delete_inputs']
                except KeyError:
                    result['delete_inputs'] = []
                result['changed'] = True
                result['delete_inputs'].append(input_name)

            pass
        for input_name in custom_block['inputs']:
            try:
                result['change_inputs']
            except KeyError:
                result['change_inputs'] = {}
            # result['changed'] = True
            result['change_inputs'][input_name] = custom_block['inputs'][input_name]

    @classmethod
    def compare_link(cls, link_name, result, block_id, custom_block, base_block, errors: list, warnings: list):
        if base_block[link_name][0] != custom_block[link_name][0] or base_block[link_name][1] != \
                custom_block[link_name][1]:
            result[link_name] = custom_block[link_name]

    @classmethod
    def compare_fields(cls, custom, base, result, block_id, custom_block, base_block, errors: list, warnings: list):
        base_fields = base.find_fields(base_block['node'])
        custom_fields = custom.find_fields(custom_block['node'])
        custom_new = list(custom_fields.keys()) if custom_fields else {}
        if not base_fields:
            return
        for field_name in base_fields:
            custom_field_value = custom_fields.get(field_name)
            base_field_value = base_fields.get(field_name)
            if field_name in custom_fields:
                if custom_field_value != base_field_value:
                    try:
                        result['change_fields']
                    except KeyError:
                        result['change_fields'] = {}
                    result['changed'] = True
                    result['change_fields'][field_name] = (
                        # Берем сырые значения, т.к. в json переменных хранятся как объект
                        cls.workspace.find_field_by_name(custom_block['node'], field_name),
                        cls.workspace.find_field_by_name(base_block['node'], field_name)
                    )
                custom_new.remove(field_name)
            else:
                try:
                    result['delete_fields']
                except KeyError:
                    result['delete_fields'] = []
                result['changed'] = True
                result['delete_fields'].append(field_name)
        for key in custom_new:
            try:
                result['new_fields']
            except KeyError:
                result['new_fields'] = []
            result['changed'] = True
            result['new_fields'].append(key)

    @classmethod
    def compare_mutations(cls, result, block_id, custom_block, base_block, errors: list, warnings: list):
        try:
            base_mutations = cls.workspace.find_mutations(base_block['node'])
            custom_mutations = cls.workspace.find_mutations(custom_block['node'])
            if base_mutations:
                for mutations_name in base_mutations:
                    if mutations_name == 'params':
                        raise NotImplementedError()
                    else:
                        custom_value = custom_mutations.get(mutations_name)
                        base_value = base_mutations.get(mutations_name)
                        if base_value != custom_value:
                            try:
                                result['change_mutations']
                            except KeyError:
                                result['change_mutations'] = {}
                            result['changed'] = True
                            result['change_mutations'][mutations_name] = (
                                cls.workspace.find_mutation_by_name(custom_block['node'], mutations_name),
                                cls.workspace.find_mutation_by_name(base_block['node'], mutations_name)
                            )

            elif custom_mutations:
                raise NotImplementedError()
        except Exception as err:
            raise ExtException(parent=err)

    @classmethod
    def compare_field(cls, result, field_name, custom_field, base_field):
        raise NotImplementedError()

    @classmethod
    def compare_mutation(cls, result, field_name, custom_field, base_field):
        raise NotImplementedError()

