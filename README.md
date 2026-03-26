# Network Configuration Drift Detector :

Un outil de comparaison conçu pour identifier les dérives de configuration ("Configuration Drift") sur les équipements réseaux en récupérant la configuration via SSH (Netmiko) et en la comparant à une "Golden Config" de référence.

## Fonctionnalités :
- Connexion SSH directe aux équipements Cisco, Juniper, etc., via `netmiko`.
- Comparaison instantanée et surbrillance des différences (ajouts en vert, retraits en rouge) grâce à `colorama`.

- Détection proactive des modifications "out-of-band" non documentées.

## Installation :
```bash
git clone https://github.com/FilouCosmos/net-config-drift-detector.git
cd net-config-drift-detector
pip install -r requirements.txt