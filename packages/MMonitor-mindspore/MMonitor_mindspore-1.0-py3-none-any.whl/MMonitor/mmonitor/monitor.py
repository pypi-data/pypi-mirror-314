from collections import defaultdict
import mindspore
import mindspore.nn as nn
from MMonitor.utils.schedules import ScheduleSelector, linear
from MMonitor.utils.register import Register
from MMonitor.quantity import QuantitySelector

class Monitor:
    def __init__(self, model, configer=None):
        self.model = model
        self.params = list(model.get_parameters())
        self.output = defaultdict(dict)
        self.configer = configer or {}
        self.parse_module, self.parse_quantity = self._config_parser()
        
        if self.configer:
            self._register()

    def track(self, global_step,addition=None):
        for quantities in self.parse_quantity.values():
            for quantity in quantities:
                if addition is not None:
                    addition_hook = type(quantity).__name__
                    module = quantity._module
                    if 'BackwardOutput' in addition_hook:
                        setattr(module,'output_grad',addition)
                    elif 'BackwardInput' in addition_hook:
                        setattr(module,'input_grad',addition)
                quantity.track(global_step)

    def get_output(self):
        self._update_output()
        return self.output

    def clean_mem(self):
        self.output.clear()
        for quantities in self.parse_quantity.values():
            for quantity in quantities:
                quantity.clean_mem()

    def _parse_quantities(self, quantities):
        quantities_list = []
        track_schedule_list = []
        
        for item in quantities:
            if isinstance(item, str):
                quantities_list.append(item)
                track_schedule_list.append(linear())
            else:
                track_schedule_list.append(
                    linear() if len(item) == 1 else ScheduleSelector.select(item[1])
                )
                quantities_list.append(item[0])
                
        return zip(quantities_list, track_schedule_list)
    def _config_parser(self):
        parse_module = defaultdict(dict)
        parse_quantity = defaultdict(dict)
        for module_name, quantities in self.configer.items():
            try:
                module = self._get_submodule(module_name)
                module.name = module_name
                parse_module[module_name] = module
                parse_quantity[module_name] = [QuantitySelector.select(quantity)(module, track_schedule) for quantity,  track_schedule in
                                               self._parse_quantities(quantities)]
            except (AttributeError, TypeError):
                for name, module in self.model.cells_and_names():
                    if self._is_module(module_name, module) and name not in parse_module.keys():
                        module.name = name
                        parse_module[name] = module
                        parse_quantity[name] = [QuantitySelector.select(quantity)(module, track_schedule) for quantity,  track_schedule in
                                               self._parse_quantities(quantities)]
        return parse_module, parse_quantity

    def _get_submodule(self, target):
        if target == "":
            return self.model
        atoms = target.split(".")
        mod = self.model
        for item in atoms:
            if not hasattr(mod, item):
                raise AttributeError(mod.__class__.__name__ + " has no attribute `" + item + "`")
            if isinstance(mod, nn.SequentialCell) or isinstance(mod, nn.ModuleList):
                if isinstance(item, str) and len(item) > 10:
                    item = item.split('_')[-1]
                mod = mod[int(item)]
            else:
                mod = getattr(mod, item)
            if not isinstance(mod, nn.Cell):
                raise AttributeError("`" + item + "` is not an nn.Module")
        return mod

    
    def _is_module(self, module_name, module):
        if isinstance(module_name, str):
            if module.__class__.__name__ == module_name:
                return True
            else:
                return False
        elif isinstance(module_name, type):
            if isinstance(module, module_name):
                return True
            else:
                return False
        else:
            return False
    def forward_input_hook_fn(monitor,cell, grad_input,grad_output):
        inputs  = grad_input[0]
        setattr(cell, 'input', inputs) 
    def forward_output_hook_fn(monitor,cell, grad_input,grad_output):
        output  = grad_output[0]
        setattr(cell, 'output', output) 
    def _register(self):
        for module_name, quantities in self.parse_quantity.items():
            module = self.parse_module[module_name]
            for quantity in quantities:
                quantity_name = type(quantity).__name__
                # 根据quantity_name的名称来判断需要设置的hook类型
                if 'ForwardInput' in quantity_name:
                    # 注册前向hook
                    module.register_forward_hook(self.forward_input_hook_fn)
                elif 'ForwardOutput' in quantity_name:
                    module.register_forward_hook(self.forward_output_hook_fn)

    def _update_output(self):
        for module_name, quantities in self.parse_quantity.items():
            for quantity in quantities:
                self.output[module_name][quantity.__class__.__name__] = quantity.get_output()

    def _process_duplicate_extensions(self, extensions):
        ext_dict = {}
        no_duplicate_ext = []

        for es in extensions:
            for extension in es:
                if type(extension) not in ext_dict:
                    no_duplicate_ext.append(extension)
                    ext_dict[type(extension)] = True

        return no_duplicate_ext
