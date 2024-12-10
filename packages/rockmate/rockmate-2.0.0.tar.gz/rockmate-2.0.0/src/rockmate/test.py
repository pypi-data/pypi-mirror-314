
def make_autograd_function(module):
        RkMod = module

        # -> so we can access to it inside the following class definition
        #  (when defining a Class inside a Class we cannot use `self`)
        class RK_autograd_Function(torch.autograd.Function):
            # === OUR FORWARD FUNCTION ===
            @staticmethod
            def forward(ctx, dummy_input, *args):
                if RkMod.compiler.storage.ld != {}:
                    ctx.RK_Storage = storage = RkMod.compiler.storage
                    ctx.name_of_inputs_which_req_grad = (
                        RkMod.name_of_inputs_which_req_grad_buffer
                    )
                    with torch.enable_grad():
                        exec(RkMod.init_code, RkMod.gd, storage.ld)  # is compiler.gd
                        # for l in RkMod.fwd_fct_list:
                        #     RkMod._exec(l)
                        for op in self.op_list[:self.op_sched.loss_idx]:
                            self._exec(op)
                else:
                    # *** INITIALIZATION PART ***
                    #  -> Get the inputs using the buffer (Rem 1)
                    dict_inputs = RkMod.dict_inputs_buffer
                    RkMod.dict_inputs_buffer = None
                    #  -> Create the RK_Storage for this run, and store it in ctx
                    ctx.RK_Storage = storage = RK_Storage()
                    storage.init(RkMod.gd)
                    RkMod.compiler.storage = storage
                    #  -> Store what we need to return inputs' grad (Rem 1)
                    ctx.name_of_inputs_which_req_grad = (
                        RkMod.name_of_inputs_which_req_grad_buffer
                    )
                    # RkMod.name_of_inputs_which_req_grad_buffer = None
                    #  -> Detach input tensors (Rem 3) and store all the inputs
                    dict_input_tensors_detach = dict()  #  dict : input -> detached input
                    for k, v in dict_inputs.items():
                        if isinstance(v, torch.Tensor):
                            v_d = v.detach().requires_grad_(v.requires_grad)
                            dict_input_tensors_detach[v] = v_d
                            storage.ld[k] = v_d
                        #  TODO elif iterables of Tensors ?
                        else:
                            storage.ld[k] = v
                    

                    torch.cuda.synchronize()
                    with torch.enable_grad():
                        self.init_fwd_exec()
                    torch.cuda.synchronize()

                #  *** EXECUTION PART ***
                # -> Autograd turns off itself before giving use the control.
                # -> But we need it to forward/backward each node.
                
                # -> Get the output
                # outs = [
                #     RkMod.compiler.get_val(out_node.main_target).detach().requires_grad_()
                #     for out_node in RkMod.rkgb_res.forward_and_backward_graph.list_output_data_anodes
                # ]

                outs = []
                for out_node in self.rkgb_res.forward_graph.output_nodes[:1]:
                    # print(anode)
                    RkMod.compiler.get_val(f"out_{out_node.main_target}").data = RkMod.compiler.get_val(out_node.main_target)
                    o = RkMod.compiler.get_val(f"out_{out_node.main_target}")#.detach().requires_grad_()
                    # print(o.grad_fn)
                    outs.append(o)

                if len(outs) == 1:
                    return outs[0]
                else:
                    return tuple(outs)
                # -> Remember that out have been detached from the rest during exec
                """
                ctx.set_materialize_grads(True) # as the default
                # -> so we don't have to check if grad_output is None
                # -> if outputs' grad is None Autograd fill them with zeros
                """

            # === END OF FORWARD FUNCTION ===

            """
            @staticmethod
            def setup_context(ctx,inputs,outputs):
                pass
            # PyTorch prefer to handle the ctx in a separate method,
            # but it makes more sense for us to handle ctx during the forward.
            # (Also, setup_context can only access to inputs and outputs,
            # so they suggest to pass intermediate values as outputs,
            # but outputs can only be tensors)
            # Anyway, it's not important, Autograd is originally designed
            # to handle the ctx during the forward, it's just that PyTorch 2.0
            # now prefers to use this separate method.
            """

            # === OUR BACKWARD FUNCTION ===
            @staticmethod
            @torch.autograd.function.once_differentiable
            def backward(ctx, *grad_outs):  #  TODO multiple outputs
                #  -> Reload the storage and out
                storage = ctx.RK_Storage
                RkMod.compiler.storage = storage
                # -> Put grad_out in out.grad (Rem 4)
                # print(grad_outs)
                # for out_mt, out_grad in zip(RkMod.rkgb_res.S_graph.outputs, grad_outs):
                for out_node, out_grad in zip(
                    self.rkgb_res.forward_and_backward_graph.list_output_data_anodes,
                    grad_outs):
                    out_mt = out_node.main_target
                    out = RkMod.compiler.get_val(out_mt)
                    # out.grad = out_grad.view(out.shape)
                    out.grad = out_grad.data.as_strided_(
                                out.shape, out.stride(), out.storage_offset()
                            )
                    out_grad.data = torch.empty(0)
                # for out_node in self.rkgb_res.forward_graph.output_nodes:
                #         # print(anode)
                #         RkMod.compiler.get_val(f"out_{out_node.main_target}").data = torch.empty(0)
                    
                #  * record_mem stuff *
                if RkMod.exec_with_record_mem:
                    RkMod.output_size = tensor_memory_size(
                        storage.ld[RkMod.output.main_target]
                    )
                    loss_idx = len(RkMod.allo_mem)
                    # self.allo_mem[-1] += self.output.info.memsize
                    # output grad is generated outside
                # -> exec bwd_fct_list with early stop or not
                stop = RkMod.backward_stop
                if stop:
                    len_fwd = len(RkMod.fwd_fct_list)
                    for l in RkMod.bwd_fct_list[: (stop - len_fwd)]:
                        with torch.enable_grad():
                            RkMod._exec(l)
                else:
                    # for l in RkMod.bwd_fct_list:
                    #     with torch.enable_grad():
                    #         RkMod._exec(l)
                    for op in RkMod.op_list[RkMod.op_sched.loss_idx+1:]:
                        RkMod._exec(op)
                    if RkMod.exec_with_record_mem and RkMod.backward_add_output_grad:
                        RkMod.allo_mem[loss_idx] += RkMod.output_size
                    #  -> return grad of dummy input + inputs' which req grad (Rem 1)
                    grad_inputs = tuple(
                        RkMod.compiler.get_val(inp).grad
                        for inp in ctx.name_of_inputs_which_req_grad
                    )
                    grads = (torch.ones(1),) + grad_inputs
                    #  -> Clear the compiler (and Autograd clears ctx)
                    # RkMod.compiler.storage = None
                    for out_node in self.rkgb_res.forward_graph.output_nodes:
                        # print(anode)
                        RkMod.compiler.get_val(f"out_{out_node.main_target}").data = torch.empty(0)
                        
                    return grads

            # === END OF BACKWARD FUNCTION ===

        return RK_autograd_Function
