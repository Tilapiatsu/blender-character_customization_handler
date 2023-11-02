from .custo_label_properties import (CustoLabelProperties, 
                                    CustoLabelCategoryProperties,
                                    CustoPartLabelProperties,
                                    CustoPartLabelCategoryProperties,
                                    UL_CustoLabel, 
                                    UL_CustoLabelCategory,
                                    UL_CustoPartLabel,
                                    UL_CustoPartLabelCategory)

from .custo_slot_properties import (CustoSlotProperties,
                                    CustoPartSlotsProperties, 
                                    CustoPartSlotsKeepLowerLayerProperties, 
                                    UL_CustoSlot,
                                    UL_CustoPartSlots)

classes = (CustoSlotProperties, 
           CustoLabelProperties,
           CustoPartLabelProperties,
           CustoPartLabelCategoryProperties,
           CustoLabelCategoryProperties, 
           CustoPartSlotsProperties, 
           CustoPartSlotsKeepLowerLayerProperties, 
           UL_CustoSlot, 
           UL_CustoLabel, 
           UL_CustoLabelCategory,
           UL_CustoPartSlots,
           UL_CustoPartLabel,
           UL_CustoPartLabelCategory)