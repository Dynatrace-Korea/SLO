README.md

A Python-based scripts used when conducting SLO related works in bulk
After modifying dtenv.properties, execute other scripts.

1_ServiceTag.py
Apply the service tag to all services starting with the parameter
E.g.) python 1_ServiceTag.py book – Apply the “book” tag to all services whose names start with “book”

2_SloSuccess.py
Create service success rate SLO of the management zone with the parameter
E.g.) python 2_SloSuccess.py book – Create service success rate SLO for “book” management zone

3_CalcMetric.py
Create calculated metric for performance SLO of the management zone with the parament
E.g.) python 3_CalcMetric.py book – Create a calculated metric for “book” management zone

4_SloPerf.py
Create service performance SLO of the management zone with the parameter
E.g.) python 4_SloPerf.py book – create performance SLO for “book” management zone

5_Slo_Dashboard.py
Create the SLO dashboard skeleton

6_Slo_MZ_Dashboard.py
Create performance SLO analysis dashboard of the management zone with the parameter
E.g.) 6_Slo_MZ_Dashboard.py book – create performance SLO analysis dashboard for “book” management zone
