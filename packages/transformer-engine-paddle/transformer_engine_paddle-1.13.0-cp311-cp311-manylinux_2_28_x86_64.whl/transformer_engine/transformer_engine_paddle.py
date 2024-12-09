import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_rmsnorm_fwd_fp8(input,weight,scale,_amax,_scaleinv,eps,index,otype,sm_margin,zero_centered_gamma):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_rmsnorm_fwd_fp8", input,weight,scale,_amax,_scaleinv,eps,index,otype,sm_margin,zero_centered_gamma)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Weight' : weight,'Scale' : scale,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['Output','InvVariance','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_rmsnorm_fwd_fp8", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        outs['InvVariance'] = helper.create_variable(dtype='float32')
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_rmsnorm_fwd_fp8", inputs=ins, outputs=outs, attrs={'eps' : eps,'index' : index,'otype' : otype,'sm_margin' : sm_margin,'zero_centered_gamma' : zero_centered_gamma})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_dswiglu(grad,input,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_dswiglu", grad,input,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Grad' : grad,'Input' : input}
        outs = {}
        outs_list = ['Output']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_dswiglu", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_dswiglu", inputs=ins, outputs=outs, attrs={'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_scaled_softmax_backward(out_grad_,softmax_results,scale_factor):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_scaled_softmax_backward", out_grad_,softmax_results,scale_factor)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'out_grad_' : out_grad_,'softmax_results' : softmax_results}
        outs = {}
        outs_list = ['out_grad']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_scaled_softmax_backward", **locals())

        outs['out_grad'] = out_grad_
        helper.append_op(type="te_scaled_softmax_backward", inputs=ins, outputs=outs, attrs={'scale_factor' : scale_factor})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def update_latest_amax_history_inplace(_history,amax):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("update_latest_amax_history_inplace", _history,amax)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'_history' : _history,'amax' : amax}
        outs = {}
        outs_list = ['history']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("update_latest_amax_history_inplace", **locals())

        outs['history'] = _history
        helper.append_op(type="update_latest_amax_history_inplace", inputs=ins, outputs=outs, attrs={})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_rmsnorm_bwd(dz,x,rsigma,gamma,sm_margin,zero_centered_gamma):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_rmsnorm_bwd", dz,x,rsigma,gamma,sm_margin,zero_centered_gamma)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Dz' : dz,'X' : x,'Rsigma' : rsigma,'Gamma' : gamma}
        outs = {}
        outs_list = ['Dx','Dgamma']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_rmsnorm_bwd", **locals())

        outs['Dx'] = helper.create_variable(dtype='float32')
        outs['Dgamma'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_rmsnorm_bwd", inputs=ins, outputs=outs, attrs={'sm_margin' : sm_margin,'zero_centered_gamma' : zero_centered_gamma})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_cast_transpose(input,scale,_castedoutput,_transposedoutput,_amax,_scaleinv,index,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_cast_transpose", input,scale,_castedoutput,_transposedoutput,_amax,_scaleinv,index,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Scale' : scale,'_CastedOutput' : _castedoutput,'_TransposedOutput' : _transposedoutput,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['CastedOutput','TransposedOutput','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_cast_transpose", **locals())

        outs['CastedOutput'] = _castedoutput
        outs['TransposedOutput'] = _transposedoutput
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_cast_transpose", inputs=ins, outputs=outs, attrs={'index' : index,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def mask_to_cu_seqlens(mask,_q_cu_seqlen,_kv_cu_seqlen,q_seqlen,kv_seqlen,need_kv):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("mask_to_cu_seqlens", mask,_q_cu_seqlen,_kv_cu_seqlen,q_seqlen,kv_seqlen,need_kv)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        if _kv_cu_seqlen is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'mask' : mask,'_q_cu_seqlen' : _q_cu_seqlen,'_kv_cu_seqlen@OPTIONAL' : _kv_cu_seqlen}
        outs = {}
        outs_list = ['q_cu_seqlen','kv_cu_seqlen@OPTIONAL']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("mask_to_cu_seqlens", **locals())

        outs['q_cu_seqlen'] = _q_cu_seqlen
        if _kv_cu_seqlen is not None:
            outs['kv_cu_seqlen@OPTIONAL'] = _kv_cu_seqlen
        helper.append_op(type="mask_to_cu_seqlens", inputs=ins, outputs=outs, attrs={'q_seqlen' : q_seqlen,'kv_seqlen' : kv_seqlen,'need_kv' : need_kv})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_scaled_softmax_forward(input,scale_factor):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_scaled_softmax_forward", input,scale_factor)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'input' : input}
        outs = {}
        outs_list = ['softmax_results']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_scaled_softmax_forward", **locals())

        outs['softmax_results'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_scaled_softmax_forward", inputs=ins, outputs=outs, attrs={'scale_factor' : scale_factor})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_fused_attn_bwd_qkvpacked(qkv,cu_seqlens,o,do,softmax_aux,_dqkv,_dbias,rng_state,b,h,d,total_seqs,max_seqlen,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,deterministic):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_fused_attn_bwd_qkvpacked", qkv,cu_seqlens,o,do,softmax_aux,_dqkv,_dbias,rng_state,b,h,d,total_seqs,max_seqlen,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,deterministic)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        if _dbias is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'QKV' : qkv,'cu_seqlens' : cu_seqlens,'O' : o,'dO' : do,'softmax_aux' : softmax_aux,'_dQKV' : _dqkv,'_dBias@OPTIONAL' : _dbias,'rng_state' : rng_state}
        outs = {}
        outs_list = ['dQKV','dBias@OPTIONAL']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_fused_attn_bwd_qkvpacked", **locals())

        outs['dQKV'] = _dqkv
        if _dbias is not None:
            outs['dBias@OPTIONAL'] = _dbias
        helper.append_op(type="te_fused_attn_bwd_qkvpacked", inputs=ins, outputs=outs, attrs={'b' : b,'h' : h,'d' : d,'total_seqs' : total_seqs,'max_seqlen' : max_seqlen,'attn_scale' : attn_scale,'p_dropout' : p_dropout,'qkv_layout' : qkv_layout,'bias_type' : bias_type,'attn_mask_type' : attn_mask_type,'qkv_type' : qkv_type,'deterministic' : deterministic})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_cast_transpose_bgrad_dgelu(gradoutput,geluinput,scale,_amax,_scaleinv,index,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_cast_transpose_bgrad_dgelu", gradoutput,geluinput,scale,_amax,_scaleinv,index,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'GradOutput' : gradoutput,'GeluInput' : geluinput,'Scale' : scale,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['CastedDgelu','TransposedDgelu','Dbias','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_cast_transpose_bgrad_dgelu", **locals())

        outs['CastedDgelu'] = helper.create_variable(dtype='float32')
        outs['TransposedDgelu'] = helper.create_variable(dtype='float32')
        outs['Dbias'] = helper.create_variable(dtype='float32')
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_cast_transpose_bgrad_dgelu", inputs=ins, outputs=outs, attrs={'index' : index,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_fused_attn_fwd_kvpacked(q,kv,cu_seqlens_q,cu_seqlens_kv,bias,_o,_softmax_aux,_rng_state,b,h,d,total_seqs_q,total_seqs_kv,max_seqlen_q,max_seqlen_kv,is_training,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,rng_elts_per_thread):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_fused_attn_fwd_kvpacked", q,kv,cu_seqlens_q,cu_seqlens_kv,bias,_o,_softmax_aux,_rng_state,b,h,d,total_seqs_q,total_seqs_kv,max_seqlen_q,max_seqlen_kv,is_training,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,rng_elts_per_thread)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        if _softmax_aux is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Q' : q,'KV' : kv,'cu_seqlens_q' : cu_seqlens_q,'cu_seqlens_kv' : cu_seqlens_kv,'Bias@OPTIONAL' : bias,'_O' : _o,'_softmax_aux@OPTIONAL' : _softmax_aux,'_rng_state' : _rng_state}
        outs = {}
        outs_list = ['O','softmax_aux@OPTIONAL','rng_state']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_fused_attn_fwd_kvpacked", **locals())

        outs['O'] = _o
        if _softmax_aux is not None:
            outs['softmax_aux@OPTIONAL'] = _softmax_aux
        outs['rng_state'] = _rng_state
        helper.append_op(type="te_fused_attn_fwd_kvpacked", inputs=ins, outputs=outs, attrs={'b' : b,'h' : h,'d' : d,'total_seqs_q' : total_seqs_q,'total_seqs_kv' : total_seqs_kv,'max_seqlen_q' : max_seqlen_q,'max_seqlen_kv' : max_seqlen_kv,'is_training' : is_training,'attn_scale' : attn_scale,'p_dropout' : p_dropout,'qkv_layout' : qkv_layout,'bias_type' : bias_type,'attn_mask_type' : attn_mask_type,'qkv_type' : qkv_type,'rng_elts_per_thread' : rng_elts_per_thread})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def cast_to_fp8(input,scale,_output,_amax,_scaleinv,index,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("cast_to_fp8", input,scale,_output,_amax,_scaleinv,index,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Scale' : scale,'_Output' : _output,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['Output','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("cast_to_fp8", **locals())

        outs['Output'] = _output
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="cast_to_fp8", inputs=ins, outputs=outs, attrs={'index' : index,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_gemm(a,a_scale_inverse,b,b_scale_inverse,bias,_d,_d_scale,_d_amax,_pre_gelu_out,_workspace,a_index,b_index,d_index,a_type,b_type,d_type,bias_type,transa,transb,grad,workspace_size,accumulate,use_split_accumulator,math_sm_count):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_gemm", a,a_scale_inverse,b,b_scale_inverse,bias,_d,_d_scale,_d_amax,_pre_gelu_out,_workspace,a_index,b_index,d_index,a_type,b_type,d_type,bias_type,transa,transb,grad,workspace_size,accumulate,use_split_accumulator,math_sm_count)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        if _d_scale is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        if _d_amax is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        if _pre_gelu_out is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'A' : a,'A_scale_inverse@OPTIONAL' : a_scale_inverse,'B' : b,'B_scale_inverse@OPTIONAL' : b_scale_inverse,'bias@OPTIONAL' : bias,'_D' : _d,'_D_scale@OPTIONAL' : _d_scale,'_D_amax@OPTIONAL' : _d_amax,'_pre_gelu_out@OPTIONAL' : _pre_gelu_out,'_workspace' : _workspace}
        outs = {}
        outs_list = ['D','D_scale@OPTIONAL','D_amax@OPTIONAL','pre_gelu_out@OPTIONAL','workspace']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_gemm", **locals())

        outs['D'] = _d
        if _d_scale is not None:
            outs['D_scale@OPTIONAL'] = _d_scale
        if _d_amax is not None:
            outs['D_amax@OPTIONAL'] = _d_amax
        if _pre_gelu_out is not None:
            outs['pre_gelu_out@OPTIONAL'] = _pre_gelu_out
        outs['workspace'] = _workspace
        helper.append_op(type="te_gemm", inputs=ins, outputs=outs, attrs={'A_index' : a_index,'B_index' : b_index,'D_index' : d_index,'A_type' : a_type,'B_type' : b_type,'D_type' : d_type,'bias_type' : bias_type,'transa' : transa,'transb' : transb,'grad' : grad,'workspace_size' : workspace_size,'accumulate' : accumulate,'use_split_accumulator' : use_split_accumulator,'math_sm_count' : math_sm_count})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def amax_and_scale_update_inplace_legacy(_amax_history,_scale,_scale_inv,non_weight_mask,current_step_id_tensor,update_weight_scale_inv,fwd_update,fp8_max,margin,amax_compute):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("amax_and_scale_update_inplace_legacy", _amax_history,_scale,_scale_inv,non_weight_mask,current_step_id_tensor,update_weight_scale_inv,fwd_update,fp8_max,margin,amax_compute)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'_amax_history' : _amax_history,'_scale' : _scale,'_scale_inv' : _scale_inv,'non_weight_mask' : non_weight_mask,'current_step_id_tensor@OPTIONAL' : current_step_id_tensor}
        outs = {}
        outs_list = ['amax_history','scale','scale_inv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("amax_and_scale_update_inplace_legacy", **locals())

        outs['amax_history'] = _amax_history
        outs['scale'] = _scale
        outs['scale_inv'] = _scale_inv
        helper.append_op(type="amax_and_scale_update_inplace_legacy", inputs=ins, outputs=outs, attrs={'update_weight_scale_inv' : update_weight_scale_inv,'fwd_update' : fwd_update,'fp8_max' : fp8_max,'margin' : margin,'amax_compute' : amax_compute})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_fused_attn_bwd(q,k,v,cu_seqlens_q,cu_seqlens_kv,o,do,softmax_aux,_dq,_dk,_dv,_dbias,rng_state,b,h,d,max_seqlen_q,max_seqlen_kv,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,deterministic):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_fused_attn_bwd", q,k,v,cu_seqlens_q,cu_seqlens_kv,o,do,softmax_aux,_dq,_dk,_dv,_dbias,rng_state,b,h,d,max_seqlen_q,max_seqlen_kv,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,deterministic)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        if _dbias is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Q' : q,'K' : k,'V' : v,'cu_seqlens_q' : cu_seqlens_q,'cu_seqlens_kv' : cu_seqlens_kv,'O' : o,'dO' : do,'softmax_aux' : softmax_aux,'_dQ' : _dq,'_dK' : _dk,'_dV' : _dv,'_dBias@OPTIONAL' : _dbias,'rng_state' : rng_state}
        outs = {}
        outs_list = ['dQ','dK','dV','dBias@OPTIONAL']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_fused_attn_bwd", **locals())

        outs['dQ'] = _dq
        outs['dK'] = _dk
        outs['dV'] = _dv
        if _dbias is not None:
            outs['dBias@OPTIONAL'] = _dbias
        helper.append_op(type="te_fused_attn_bwd", inputs=ins, outputs=outs, attrs={'b' : b,'h' : h,'d' : d,'max_seqlen_q' : max_seqlen_q,'max_seqlen_kv' : max_seqlen_kv,'attn_scale' : attn_scale,'p_dropout' : p_dropout,'qkv_layout' : qkv_layout,'bias_type' : bias_type,'attn_mask_type' : attn_mask_type,'qkv_type' : qkv_type,'deterministic' : deterministic})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_fused_attn_fwd_qkvpacked(qkv,cu_seqlens,bias,_o,_softmax_aux,_rng_state,b,h,d,total_seqs,max_seqlen,is_training,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,rng_elts_per_thread):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_fused_attn_fwd_qkvpacked", qkv,cu_seqlens,bias,_o,_softmax_aux,_rng_state,b,h,d,total_seqs,max_seqlen,is_training,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,rng_elts_per_thread)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        if _softmax_aux is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'QKV' : qkv,'cu_seqlens' : cu_seqlens,'Bias@OPTIONAL' : bias,'_O' : _o,'_softmax_aux@OPTIONAL' : _softmax_aux,'_rng_state' : _rng_state}
        outs = {}
        outs_list = ['O','softmax_aux@OPTIONAL','rng_state']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_fused_attn_fwd_qkvpacked", **locals())

        outs['O'] = _o
        if _softmax_aux is not None:
            outs['softmax_aux@OPTIONAL'] = _softmax_aux
        outs['rng_state'] = _rng_state
        helper.append_op(type="te_fused_attn_fwd_qkvpacked", inputs=ins, outputs=outs, attrs={'b' : b,'h' : h,'d' : d,'total_seqs' : total_seqs,'max_seqlen' : max_seqlen,'is_training' : is_training,'attn_scale' : attn_scale,'p_dropout' : p_dropout,'qkv_layout' : qkv_layout,'bias_type' : bias_type,'attn_mask_type' : attn_mask_type,'qkv_type' : qkv_type,'rng_elts_per_thread' : rng_elts_per_thread})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_gelu_fp8(input,scale,_amax,_scaleinv,index,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_gelu_fp8", input,scale,_amax,_scaleinv,index,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Scale' : scale,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['Output','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_gelu_fp8", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_gelu_fp8", inputs=ins, outputs=outs, attrs={'index' : index,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def amax_and_scale_update_inplace(_amax_history,_scale,_scale_inv,non_weight_mask,fp8_dtype,margin,amax_compute):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("amax_and_scale_update_inplace", _amax_history,_scale,_scale_inv,non_weight_mask,fp8_dtype,margin,amax_compute)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'_amax_history' : _amax_history,'_scale' : _scale,'_scale_inv' : _scale_inv,'non_weight_mask' : non_weight_mask}
        outs = {}
        outs_list = ['amax_history','scale','scale_inv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("amax_and_scale_update_inplace", **locals())

        outs['amax_history'] = _amax_history
        outs['scale'] = _scale
        outs['scale_inv'] = _scale_inv
        helper.append_op(type="amax_and_scale_update_inplace", inputs=ins, outputs=outs, attrs={'fp8_dtype' : fp8_dtype,'margin' : margin,'amax_compute' : amax_compute})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_scaled_masked_softmax_backward(out_grad_,softmax_results,scale_factor):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_scaled_masked_softmax_backward", out_grad_,softmax_results,scale_factor)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'out_grad_' : out_grad_,'softmax_results' : softmax_results}
        outs = {}
        outs_list = ['out_grad']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_scaled_masked_softmax_backward", **locals())

        outs['out_grad'] = out_grad_
        helper.append_op(type="te_scaled_masked_softmax_backward", inputs=ins, outputs=outs, attrs={'scale_factor' : scale_factor})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_layernorm_bwd(dz,x,mu,rsigma,gamma,sm_margin,zero_centered_gamma):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_layernorm_bwd", dz,x,mu,rsigma,gamma,sm_margin,zero_centered_gamma)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Dz' : dz,'X' : x,'Mu' : mu,'Rsigma' : rsigma,'Gamma' : gamma}
        outs = {}
        outs_list = ['Dx','Dgamma','Dbeta']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_layernorm_bwd", **locals())

        outs['Dx'] = helper.create_variable(dtype='float32')
        outs['Dgamma'] = helper.create_variable(dtype='float32')
        outs['Dbeta'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_layernorm_bwd", inputs=ins, outputs=outs, attrs={'sm_margin' : sm_margin,'zero_centered_gamma' : zero_centered_gamma})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_gelu(input,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_gelu", input,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input}
        outs = {}
        outs_list = ['Output']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_gelu", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_gelu", inputs=ins, outputs=outs, attrs={'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_fused_attn_fwd(q,k,v,cu_seqlens_q,cu_seqlens_kv,bias,_o,_softmax_aux,_rng_state,b,h,d,max_seqlen_q,max_seqlen_kv,is_training,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,rng_elts_per_thread):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_fused_attn_fwd", q,k,v,cu_seqlens_q,cu_seqlens_kv,bias,_o,_softmax_aux,_rng_state,b,h,d,max_seqlen_q,max_seqlen_kv,is_training,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,rng_elts_per_thread)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        if _softmax_aux is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Q' : q,'K' : k,'V' : v,'cu_seqlens_q' : cu_seqlens_q,'cu_seqlens_kv' : cu_seqlens_kv,'Bias@OPTIONAL' : bias,'_O' : _o,'_softmax_aux@OPTIONAL' : _softmax_aux,'_rng_state' : _rng_state}
        outs = {}
        outs_list = ['O','softmax_aux@OPTIONAL','rng_state']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_fused_attn_fwd", **locals())

        outs['O'] = _o
        if _softmax_aux is not None:
            outs['softmax_aux@OPTIONAL'] = _softmax_aux
        outs['rng_state'] = _rng_state
        helper.append_op(type="te_fused_attn_fwd", inputs=ins, outputs=outs, attrs={'b' : b,'h' : h,'d' : d,'max_seqlen_q' : max_seqlen_q,'max_seqlen_kv' : max_seqlen_kv,'is_training' : is_training,'attn_scale' : attn_scale,'p_dropout' : p_dropout,'qkv_layout' : qkv_layout,'bias_type' : bias_type,'attn_mask_type' : attn_mask_type,'qkv_type' : qkv_type,'rng_elts_per_thread' : rng_elts_per_thread})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_layernorm_fwd(input,weight,bias,eps,otype,sm_margin,zero_centered_gamma):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_layernorm_fwd", input,weight,bias,eps,otype,sm_margin,zero_centered_gamma)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Weight' : weight,'Bias' : bias}
        outs = {}
        outs_list = ['Output','Mu','Rsigma']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_layernorm_fwd", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        outs['Mu'] = helper.create_variable(dtype='float32')
        outs['Rsigma'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_layernorm_fwd", inputs=ins, outputs=outs, attrs={'eps' : eps,'otype' : otype,'sm_margin' : sm_margin,'zero_centered_gamma' : zero_centered_gamma})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_scaled_masked_softmax_forward(input,mask,scale_factor):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_scaled_masked_softmax_forward", input,mask,scale_factor)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'input' : input,'mask' : mask}
        outs = {}
        outs_list = ['softmax_results']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_scaled_masked_softmax_forward", **locals())

        outs['softmax_results'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_scaled_masked_softmax_forward", inputs=ins, outputs=outs, attrs={'scale_factor' : scale_factor})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_fused_attn_bwd_kvpacked(q,kv,cu_seqlens_q,cu_seqlens_kv,o,do,softmax_aux,_dq,_dkv,_dbias,rng_state,b,h,d,total_seqs_q,total_seqs_kv,max_seqlen_q,max_seqlen_kv,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,deterministic):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_fused_attn_bwd_kvpacked", q,kv,cu_seqlens_q,cu_seqlens_kv,o,do,softmax_aux,_dq,_dkv,_dbias,rng_state,b,h,d,total_seqs_q,total_seqs_kv,max_seqlen_q,max_seqlen_kv,attn_scale,p_dropout,qkv_layout,bias_type,attn_mask_type,qkv_type,deterministic)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        if _dbias is not None:
            res.append(outs[start_idx])
        else:
            res.append(None)
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Q' : q,'KV' : kv,'cu_seqlens_q' : cu_seqlens_q,'cu_seqlens_kv' : cu_seqlens_kv,'O' : o,'dO' : do,'softmax_aux' : softmax_aux,'_dQ' : _dq,'_dKV' : _dkv,'_dBias@OPTIONAL' : _dbias,'rng_state' : rng_state}
        outs = {}
        outs_list = ['dQ','dKV','dBias@OPTIONAL']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_fused_attn_bwd_kvpacked", **locals())

        outs['dQ'] = _dq
        outs['dKV'] = _dkv
        if _dbias is not None:
            outs['dBias@OPTIONAL'] = _dbias
        helper.append_op(type="te_fused_attn_bwd_kvpacked", inputs=ins, outputs=outs, attrs={'b' : b,'h' : h,'d' : d,'total_seqs_q' : total_seqs_q,'total_seqs_kv' : total_seqs_kv,'max_seqlen_q' : max_seqlen_q,'max_seqlen_kv' : max_seqlen_kv,'attn_scale' : attn_scale,'p_dropout' : p_dropout,'qkv_layout' : qkv_layout,'bias_type' : bias_type,'attn_mask_type' : attn_mask_type,'qkv_type' : qkv_type,'deterministic' : deterministic})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_swiglu_fp8(input,scale,_amax,_scaleinv,index,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_swiglu_fp8", input,scale,_amax,_scaleinv,index,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Scale' : scale,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['Output','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_swiglu_fp8", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_swiglu_fp8", inputs=ins, outputs=outs, attrs={'index' : index,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_scaled_upper_triang_masked_softmax_forward(input,scale_factor):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_scaled_upper_triang_masked_softmax_forward", input,scale_factor)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'input' : input}
        outs = {}
        outs_list = ['softmax_results']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_scaled_upper_triang_masked_softmax_forward", **locals())

        outs['softmax_results'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_scaled_upper_triang_masked_softmax_forward", inputs=ins, outputs=outs, attrs={'scale_factor' : scale_factor})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_transpose(input,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_transpose", input,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input}
        outs = {}
        outs_list = ['Output']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_transpose", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_transpose", inputs=ins, outputs=outs, attrs={'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_rmsnorm_fwd(input,weight,eps,otype,sm_margin,zero_centered_gamma):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_rmsnorm_fwd", input,weight,eps,otype,sm_margin,zero_centered_gamma)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Weight' : weight}
        outs = {}
        outs_list = ['Output','InvVariance']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_rmsnorm_fwd", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        outs['InvVariance'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_rmsnorm_fwd", inputs=ins, outputs=outs, attrs={'eps' : eps,'otype' : otype,'sm_margin' : sm_margin,'zero_centered_gamma' : zero_centered_gamma})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_layernorm_fwd_fp8(input,weight,bias,scale,_amax,_scaleinv,eps,index,otype,sm_margin,zero_centered_gamma):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_layernorm_fwd_fp8", input,weight,bias,scale,_amax,_scaleinv,eps,index,otype,sm_margin,zero_centered_gamma)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'Weight' : weight,'Bias' : bias,'Scale' : scale,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['Output','Mu','Rsigma','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_layernorm_fwd_fp8", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        outs['Mu'] = helper.create_variable(dtype='float32')
        outs['Rsigma'] = helper.create_variable(dtype='float32')
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_layernorm_fwd_fp8", inputs=ins, outputs=outs, attrs={'eps' : eps,'index' : index,'otype' : otype,'sm_margin' : sm_margin,'zero_centered_gamma' : zero_centered_gamma})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def cast_from_fp8(input,scaleinv,index,itype,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("cast_from_fp8", input,scaleinv,index,itype,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input,'ScaleInv' : scaleinv}
        outs = {}
        outs_list = ['Output']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("cast_from_fp8", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        helper.append_op(type="cast_from_fp8", inputs=ins, outputs=outs, attrs={'index' : index,'itype' : itype,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_cast_transpose_bgrad(gradoutput,scale,_amax,_scaleinv,index,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_cast_transpose_bgrad", gradoutput,scale,_amax,_scaleinv,index,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'GradOutput' : gradoutput,'Scale' : scale,'_Amax' : _amax,'_ScaleInv' : _scaleinv}
        outs = {}
        outs_list = ['dBias','CastedOutput','TransposedOutput','Amax','ScaleInv']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_cast_transpose_bgrad", **locals())

        outs['dBias'] = helper.create_variable(dtype='float32')
        outs['CastedOutput'] = helper.create_variable(dtype='float32')
        outs['TransposedOutput'] = helper.create_variable(dtype='float32')
        outs['Amax'] = _amax
        outs['ScaleInv'] = _scaleinv
        helper.append_op(type="te_cast_transpose_bgrad", inputs=ins, outputs=outs, attrs={'index' : index,'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_scaled_upper_triang_masked_softmax_backward(out_grad_,softmax_results,scale_factor):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_scaled_upper_triang_masked_softmax_backward", out_grad_,softmax_results,scale_factor)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'out_grad_' : out_grad_,'softmax_results' : softmax_results}
        outs = {}
        outs_list = ['out_grad']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_scaled_upper_triang_masked_softmax_backward", **locals())

        outs['out_grad'] = out_grad_
        helper.append_op(type="te_scaled_upper_triang_masked_softmax_backward", inputs=ins, outputs=outs, attrs={'scale_factor' : scale_factor})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import paddle.base.core as core
from paddle.framework import in_dynamic_mode
from paddle.base.layer_helper import LayerHelper

def te_swiglu(input,otype):
    # The output variable's dtype use default value 'float32',
    # and the actual dtype of output variable will be inferred in runtime.
    if in_dynamic_mode():
        outs = core.eager._run_custom_op("te_swiglu", input,otype)
        res = []
        start_idx = 0
        res.append(outs[start_idx])
        start_idx += 1
        return res[0] if len(res)==1 else res
    else:
        ins = {}
        ins_map = {'Input' : input}
        outs = {}
        outs_list = ['Output']
        for key, value in ins_map.items():
            # handle optional inputs
            if value is not None:
                ins[key] = value
        helper = LayerHelper("te_swiglu", **locals())

        outs['Output'] = helper.create_variable(dtype='float32')
        helper.append_op(type="te_swiglu", inputs=ins, outputs=outs, attrs={'otype' : otype})
        res = [outs[out_name] if out_name in outs.keys() else None for out_name in outs_list]
        return res[0] if len(res)==1 else res


import os
import sys
import types
import paddle
import importlib.abc
import importlib.util

cur_dir = os.path.dirname(os.path.abspath(__file__))
so_path = os.path.join(cur_dir, "transformer_engine_paddle_pd_.so")

def __bootstrap__():
    assert os.path.exists(so_path)
    # load custom op shared library with abs path
    custom_ops = paddle.utils.cpp_extension.load_op_meta_info_and_register_op(so_path)

    if os.name == 'nt' or sys.platform.startswith('darwin'):
        # Cpp Extension only support Linux now
        mod = types.ModuleType(__name__)
    else:
        try:
            spec = importlib.util.spec_from_file_location(__name__, so_path)
            assert spec is not None
            mod = importlib.util.module_from_spec(spec)
            assert isinstance(spec.loader, importlib.abc.Loader)
            spec.loader.exec_module(mod)
        except ImportError:
            mod = types.ModuleType(__name__)

    for custom_op in custom_ops:
        setattr(mod, custom_op, eval(custom_op))

__bootstrap__()

