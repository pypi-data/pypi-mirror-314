#===================================================================================================
# Orpheus Music Transformer models Python module
#===================================================================================================
# Project Los Angeles
# Tegridy Code 2024
#===================================================================================================
# License: Apache 2.0
#===================================================================================================

MODELS_HF_REPO_LINK = 'asigalov61/Orpheus-Music-Transformer'
MODELS_HF_REPO_URL = 'https://huggingface.co/asigalov61/Orpheus-Music-Transformer'

MODELS_INFO = {'medium': 'Medium current model.'
               }

MODELS_FILE_NAMES = {'medium': 'Orpheus_Music_Transformer_Medium_Trained_Model_42174_steps_0.5211_loss_0.8542_acc.pth'}

MODELS_SEQ_LEN = 8192
MODELS_PAD_IDX = 19815

MODELS_PARAMETERS = {'medium': {'dim': 2048,
                                'depth': 8,
                                'heads': 32,
                                'rope': True,
                                'params': 482
                                },
                    }

#===================================================================================================
# This is the end of models Python module
#===================================================================================================