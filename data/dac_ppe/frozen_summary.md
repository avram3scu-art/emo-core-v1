# Frozen PPE profiles (F8.8, written before the manuscript's tables were opened)

## BE

End point: municipalities. Missing: dedicated_funding, institutionalisation.

| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |
|---|---|---|---|---|
| order_3M_ffp2=A | firm_order | order_3M_ffp2 | 2020-01-31 | 1–1 |
| order_3M_ffp2=A | binding_act | am_23mar_sale | 2020-03-23 | 53–53 |
| order_3M_ffp2=A | delivery | del_communes | 2020-03-16 | 46–46 |
| order_3M_ffp2=A | delivery (secondary: federal stock (supplier delivery to SPF/Peutie)) | {'delivery_lag_from_t0': {'min_days': 50, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |
| order_3M_ffp2=A | delivery (secondary: hospitals (providers)) | {'delivery_lag_from_t0': {'min_days': 50, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |

Paired order-to-delivery lags (order_3M_ffp2=A):

- {"order_id": "order_3M_ffp2", "delivery_id": "del_3M_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 56, "max_days": 56}}
- {"order_id": "order_life_surgical", "delivery_id": "del_life_surgical", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "surgical masks", "interval": {"min_days": 5, "max_days": 5}}
- {"order_id": "order_ultrazonic_ffp2", "delivery_id": "del_ultrazonic_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 21, "max_days": 21}}
- {"order_id": "order_life_ffp2", "delivery_id": "del_life_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 10, "max_days": 10}}
- {"order_id": "order_erard_gloves", "delivery_id": "del_erard_gloves", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "gloves", "interval": {"min_days": 5, "max_days": 5}}
- {"order_id": "order_xml_surgical", "delivery_id": "del_xml_surgical", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "surgical masks", "interval": {"min_days": 6, "max_days": 6}}

Identification (order_3M_ffp2=A): {"FFP2 respirators": {"n_paired_orders": 3, "order_date_spread": {"min_days": 52, "max_days": 52}, "minimum_for_separation_met": true}, "gloves": {"n_paired_orders": 1, "order_date_spread": {"min_days": 0, "max_days": 0}, "minimum_for_separation_met": false}, "surgical masks": {"n_paired_orders": 2, "order_date_spread": {"min_days": 16, "max_days": 16}, "minimum_for_separation_met": true}}

| order_3M_ffp2=B | firm_order | order_3M_ffp2 | 2020-02-04 | 5–5 |
| order_3M_ffp2=B | binding_act | am_23mar_sale | 2020-03-23 | 53–53 |
| order_3M_ffp2=B | delivery | del_communes | 2020-03-16 | 46–46 |
| order_3M_ffp2=B | delivery (secondary: federal stock (supplier delivery to SPF/Peutie)) | {'delivery_lag_from_t0': {'min_days': 50, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |
| order_3M_ffp2=B | delivery (secondary: hospitals (providers)) | {'delivery_lag_from_t0': {'min_days': 50, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |

Paired order-to-delivery lags (order_3M_ffp2=B):

- {"order_id": "order_3M_ffp2", "delivery_id": "del_3M_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 52, "max_days": 52}}
- {"order_id": "order_life_surgical", "delivery_id": "del_life_surgical", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "surgical masks", "interval": {"min_days": 5, "max_days": 5}}
- {"order_id": "order_ultrazonic_ffp2", "delivery_id": "del_ultrazonic_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 21, "max_days": 21}}
- {"order_id": "order_life_ffp2", "delivery_id": "del_life_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 10, "max_days": 10}}
- {"order_id": "order_erard_gloves", "delivery_id": "del_erard_gloves", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "gloves", "interval": {"min_days": 5, "max_days": 5}}
- {"order_id": "order_xml_surgical", "delivery_id": "del_xml_surgical", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "surgical masks", "interval": {"min_days": 6, "max_days": 6}}

Identification (order_3M_ffp2=B): {"FFP2 respirators": {"n_paired_orders": 3, "order_date_spread": {"min_days": 48, "max_days": 48}, "minimum_for_separation_met": true}, "gloves": {"n_paired_orders": 1, "order_date_spread": {"min_days": 0, "max_days": 0}, "minimum_for_separation_met": false}, "surgical masks": {"n_paired_orders": 2, "order_date_spread": {"min_days": 16, "max_days": 16}, "minimum_for_separation_met": true}}

| order_3M_ffp2=C | firm_order | order_3M_ffp2 | 2020-03-04 | 34–34 |
| order_3M_ffp2=C | binding_act | am_23mar_sale | 2020-03-23 | 53–53 |
| order_3M_ffp2=C | delivery | del_communes | 2020-03-16 | 46–46 |
| order_3M_ffp2=C | delivery (secondary: federal stock (supplier delivery to SPF/Peutie)) | {'delivery_lag_from_t0': {'min_days': 50, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |
| order_3M_ffp2=C | delivery (secondary: hospitals (providers)) | {'delivery_lag_from_t0': {'min_days': 50, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |

Paired order-to-delivery lags (order_3M_ffp2=C):

- {"order_id": "order_3M_ffp2", "delivery_id": "del_3M_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 23, "max_days": 23}}
- {"order_id": "order_life_surgical", "delivery_id": "del_life_surgical", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "surgical masks", "interval": {"min_days": 5, "max_days": 5}}
- {"order_id": "order_ultrazonic_ffp2", "delivery_id": "del_ultrazonic_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 21, "max_days": 21}}
- {"order_id": "order_life_ffp2", "delivery_id": "del_life_ffp2", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "FFP2 respirators", "interval": {"min_days": 10, "max_days": 10}}
- {"order_id": "order_erard_gloves", "delivery_id": "del_erard_gloves", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "gloves", "interval": {"min_days": 5, "max_days": 5}}
- {"order_id": "order_xml_surgical", "delivery_id": "del_xml_surgical", "order_end_point": "municipalities", "end_point": "federal stock (supplier delivery to SPF/Peutie)", "good": "surgical masks", "interval": {"min_days": 6, "max_days": 6}}

Identification (order_3M_ffp2=C): {"FFP2 respirators": {"n_paired_orders": 3, "order_date_spread": {"min_days": 19, "max_days": 19}, "minimum_for_separation_met": true}, "gloves": {"n_paired_orders": 1, "order_date_spread": {"min_days": 0, "max_days": 0}, "minimum_for_separation_met": false}, "surgical masks": {"n_paired_orders": 2, "order_date_spread": {"min_days": 16, "max_days": 16}, "minimum_for_separation_met": true}}


## FR

End point: pharmacies supplying health professionals. Missing: institutionalisation.

| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |
|---|---|---|---|---|
| order_ffp2_28m=A | firm_order | order_ffp2_28m | 2020-02-07 | 8–8 |
| order_ffp2_28m=A | binding_act | decree_requisition | 2020-03-03 | 33–33 |
| order_ffp2_28m=A | delivery | del_pharmacies | 2020-03-09..2020-03-22 | 39–52 |
| order_ffp2_28m=B | firm_order | order_ffp2_28m | 2020-02-19 | 20–20 |
| order_ffp2_28m=B | binding_act | decree_requisition | 2020-03-03 | 33–33 |
| order_ffp2_28m=B | delivery | del_pharmacies | 2020-03-09..2020-03-22 | 39–52 |

## DE

End point: Länder and Kassenärztliche Vereinigungen. Missing: dedicated_funding, institutionalisation.

| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |
|---|---|---|---|---|
| first_order_federal=A | firm_order | first_order_federal | 2020-02-28..2020-03-09 | 29–39 |
| first_order_federal=A | binding_act | export_ban | 2020-03-04 | 34–34 |
| first_order_federal=A | delivery | del_laender_kv | 2020-03-11..2020-03-20 | 41–50 |
| first_order_federal=B | firm_order | first_order_federal | 2020-02-28..2020-03-20 | 29–50 |
| first_order_federal=B | binding_act | export_ban | 2020-03-04 | 34–34 |
| first_order_federal=B | delivery | del_laender_kv | 2020-03-11..2020-03-20 | 41–50 |

## NL

End point: regional acute-care networks (ROAZ). Missing: binding_act, dedicated_funding, institutionalisation.

| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |
|---|---|---|---|---|
| - | firm_order | first_order_national | 2020-03-06..2020-03-09 | 36–39 |
| - | delivery | del_china_690k_roaz | 2020-03-21..2020-03-22 | 51–52 |
| - | delivery (secondary: care providers) | {'delivery_lag_from_t0': {'min_days': 43, 'max_days': 50}, 'unpaired_first_order_to_first_delivery': None} | | |

## SE

End point: regions and municipalities. Missing: dedicated_funding, institutionalisation.

| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |
|---|---|---|---|---|
| - | firm_order | first_order_sos | 2020-02-01..2020-02-29 | 2–30 |
| - | binding_act | ordinance_2020_126 | 2020-03-16 | 46–46 |
| - | delivery | first_delivery_regions | 2020-03-17..2020-03-31 | 47–61 |

## EU

End point: member states. Missing: dedicated_funding, firm_order, institutionalisation.

| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |
|---|---|---|---|---|
| - | binding_act | reg_2020_402 | 2020-03-14 | 44–44 |
| - | delivery | first_resceu_delivery | 2020-04-25 | 86–86 |
| - | counter_measure | de_export_ban | 2020-03-04 | 34–34 |
