"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MISCELLANEOUS CODES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import numpy as np

''' -------------------------------------------------------------------- '''
''' Function. Create a list with 'val' replicated n times                '''
''' -------------------------------------------------------------------- '''
def make_list(val, n):
    return [val] * n

def list_of_zeros(n): # {
    return make_list(0, n)
# }

###########################################################################
# CODES COMMON TO LATENT_CLASS AND LATENT_CLASS_MIXED
###########################################################################

''' -------------------------------------------------------------------- '''
''' Function. Define as [None, None, ..., None] where |[...]| = num_classes '''
''' -------------------------------------------------------------------- '''
def initialise_avail_latent(avail_latent, num_classes):
#{
    # CONSIDER REPLACING 'None' WITH 'NaN'
    avail_latent = np.repeat(None, num_classes) if avail_latent is None else avail_latent
    return avail_latent
# }

''' -------------------------------------------------------------------- '''
''' Function. Initialise fit_intercept flag                              '''
''' -------------------------------------------------------------------- '''
def initialise_fit_intercept(params, fit_inter = None, is_latent = False):
# {
    if is_latent:
    # {
        if '_inter' in params:
            return True
        else:
            return False
    # }
    if fit_inter is not None:
    # {
        if '_inter' in params:
            return params
        return '_inter' in np.concatenate(params)
    # }
    else:
    # {
        for i in params:
            if '_inter' in i:
                return True                    
        return False
    # }
# }

''' -------------------------------------------------------------------- '''
''' Function. Initialise class_params_spec                               '''
''' If unspecified, default to using all varnames in each latent class   '''
''' -------------------------------------------------------------------- '''
def initialise_class_params_spec(class_params_spec, isvars, varnames, num_classes):
# {
    if class_params_spec is None: # {
        if isvars is not None:
            class_vars = [var for var in varnames if var not in isvars]
        else:
            class_vars = varnames

        # Replicate class_vars and vstack the replicates
        class_params_spec = np.vstack(make_list(class_vars, num_classes))
    # }
    return class_params_spec
# }

''' -------------------------------------------------------------------- '''
''' Function.                                                            '''
''' -------------------------------------------------------------------- '''
def initialise_membership_as_probability(member_params_spec):
# {
    membership_as_probability = True if member_params_spec is True else False
    return membership_as_probability
# }

''' -------------------------------------------------------------------- '''
''' Function. Initialise member_params_spec                              '''
''' -------------------------------------------------------------------- '''
def initialise_member_params_spec(membership_as_probability, member_params_spec, isvars, varnames, num_classes):
# {
    if membership_as_probability:
        member_params_spec = np.vstack(make_list('dummy', num_classes-1))  # Replicate 'dummy' and vstack the replicates

    if member_params_spec is None:
    # {
        if isvars is not None: member_vars = isvars
        else: member_vars = varnames

        # Replicate member_vars and vstack the replicates
        member_params_spec = np.vstack(make_list(member_vars, num_classes-1))
    # }
    return member_params_spec
# }

''' -------------------------------------------------------------------- '''
''' Function. Initialise intercept_opts                                  '''
''' -------------------------------------------------------------------- '''
def initialise_opts(intercept_opts, num_classes):
# {
    if intercept_opts is None:
        intercept_opts = {}
    else:
    # {
        if 'class_intercept_alts' in intercept_opts:  # {
            if len(intercept_opts['class_intercept_alts']) != num_classes:
                raise ValueError("The key class_intercept_alts in intercept_opts must be the same length as num_classes")
    # }
    return intercept_opts
# }
''' -------------------------------------------------------------------- '''
''' Function. Setup multinomial_logit or mixed_logit                     '''
''' -------------------------------------------------------------------- '''
def setup_logit(i, logit, X, y, varnames, class_params_spec, avail, alts, transvars, gtol,
    mxl=False, panels=None, randvars=None, correlated_vars=None, n_draws=None, mnl_init=None):
# {
    varnames_i, fit_intercept_i = class_params_spec[i], False
    if '_inter' in varnames_i:  
    # {
        # X = np.hstack((np.ones((X.shape[0], 1)), X))
        # if '_inter' not in varnames: #FIXME why does the interpept miss
         #   varnames = np.append(['_inter'], varnames)
        fit_intercept_i = True #this was true I am just adding it to the data
        varnames_i = [var for var in varnames_i]
        varnames_i = [var for var in varnames_i if var != '_inter']
        #varnames_i = [var for var in varnames_i if var != '_inter']           
    # }                                                                

    X_i_idx = [ii for ii, name in enumerate(varnames) if name in varnames_i]
    X_i = np.array(X)[:, X_i_idx]

    transvars_i = []
    if transvars is not None:
        transvars_i = [transvar for transvar in transvars if transvar in varnames_i]

    if mxl:
    # {
        randvars_i = {k: v for k, v in randvars.items() if k in varnames_i}
        correlated_vars_i = correlated_vars
        if correlated_vars is not None and isinstance(correlated_vars, list):
            correlated_vars_i = [corvar for corvar in correlated_vars if corvar in varnames_i]

        logit.setup(X_i, y, varnames_i, alts, avail=avail, transvars=transvars_i,
                randvars=randvars_i, panels=panels, fit_intercept=fit_intercept_i,
                correlated_vars=correlated_vars_i, n_draws=n_draws, mnl_init=mnl_init, gtol=gtol)
    # }
    else:
        logit.setup(X_i, y, varnames_i, alts, avail=avail, transvars=transvars_i,
              fit_intercept=fit_intercept_i, gtol=gtol)
    logit.fit()
    return logit
# }

''' -------------------------------------------------------------------- '''
''' Function.                                                            '''
''' -------------------------------------------------------------------- '''
def revise_betas(i, logit, betas, intercept_opts, alts):
# {
    coefs = logit.coeff_est + np.random.normal(0, 0.01, len(logit.coeff_est))  # Add some random noise
    if 'class_intercept_alts' in intercept_opts:
    # {
        intercept_idx = np.array(intercept_opts['class_intercept_alts'][i]) - 2
        J = len(np.unique(alts))  # Code shortcut
        coefs = np.concatenate((coefs[intercept_idx], coefs[(J - 1):]))
    # }
    betas[i] = coefs + np.random.normal(0, 0.01, len(coefs))  # Add small amounts of noise
    return betas
# }
