import importlib
import sys
import pkgutil
import gbdtransformation
import json

def import_submodules(package_name):
    """ Import all submodules of a module, recursively

    :param package_name: Package name
    :type package_name: str
    :rtype: dict[types.ModuleType]
    """
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }

def get_transformation_package():
    accepted_keys = ['brands', 'designs']
    all_transforms = import_submodules('gbdtransformation')
    results = {}
    for key in all_transforms.keys():
        if key in accepted_keys:
            current_transforms = import_submodules('gbdtransformation.%s' % key)
            for collection, transform in current_transforms.items():
                results[collection] = {}
                for numtype in ['appnum', 'regnum']:
                    try:
                        masks = getattr(transform, '%s_mask' % numtype)
                        if not isinstance(masks, list): masks = [masks]
                    except:
                        masks = ['(.*)']
                    results[collection][numtype] = masks
    return results

def write_masks_to_json(filename):
    with open(filename, 'w') as f:
        json.dump(get_transformation_package(), f, indent=4)

if __name__ == '__main__':
    write_masks_to_json('masks.json')