# Rapport d'Exécution — Lab Agentic Driving Coach

Ce document récapitule l'ensemble du travail expérimental, des analyses et des livrables préparés pour le lab **Agentic Driving Coach** (CSE 494 / CSE 598).

---

## 1. Tâches terminées

- [x] **Inspection préalable et validation de l'environnement :**
  - Identification de l'environnement WSL2 Ubuntu 24.04 (Python 3.12.3, venv `.venv-linux`, xronos 0.13.1, matplotlib 3.11.2).
  - Exécution du script officiel de diagnostic et génération de `results/environment.txt`.
- [x] **Partie 1 — Warm-up timing Xronos (Exemples 01 à 05) :**
  - Exécution des exemples 01 (`01_hello_reactor.py`), 02 (`02_timer_and_ports.py`), 03 (`03_logical_delay.py`), 04 (`04_deadline_lag.py`), et 05 (`05_retroactive_fallback.py`).
  - Modification expérimentale de `examples/03_logical_delay.py` (délai 500 ms -> 300 ms), prédiction vérifiée, réversion git propre.
  - Analyse approfondie du temps logique, de la latence, du lag, du slack et du fallback rétroactif (Phase A vs Phase B).
- [x] **Partie 2 — Simulations de référence déterministes :**
  - Exécution de `rule-a`, `rule-b` et `replay` en mode `--fast`.
  - Vérification de déterminisme strict entre `rule-a` et `rule-b` (seuls `run_id` et `xronos_lag` diffèrent).
  - Analyse des métriques d'arrêt (`stopped=True`, `stop_position_error_m=-4.522 m`).
  - Localisation des délais logiques (500 ms et 200 ms) dans `configs/stop_sign.toml` et `src/agentic_driving_coach/scenario.py`.
  - Analyse chronologique de l'armement de l'actionnement (t=6700 ms -> t=6800 ms -> t=7000 ms).
  - Modification de `Planner.decide` pour la désescalade verbale, prédiction vérifiée (t=4600 ms), exécution de `results/rule-deescalate`, réversion git propre.
- [x] **Partie 3 — Évaluation des modèles d'IA :**
  - Constat de l'absence de runtime GPU/Ollama local en arrière-plan.
  - Exécution conforme des traces de rejeu certifiées poste de travail (`live_llama3.2-1b_300ms.jsonl` et `live_llama3.2-3b_300ms.jsonl`) produisant `results/replay-1b-300` et `results/replay-3b-300`.
  - Synthèse et génération des artéfacts de comparaison `results/model-comparison/` (`comparison.csv`, `comparison.json`, `comparison.png`).
  - Analyse du compromis latence vs qualité (taux de dépassement de deadline, réponses malformées, faux négatifs non sécurisés).
- [x] **Partie 4 — Comparaison des profils de conduite :**
  - Exécution de `coach compare-behaviors` pour `beginner` vs `advanced` (3 répétitions chacune).
  - Production des artéfacts `results/behavior-comparison/` (`comparison.csv`, `comparison.json`, `comparison.png`).
  - Interprétation de l'influence du profil conducteur sur les violations de bande de sécurité, les actionnements d'urgence et la marge d'arrêt.
- [x] **Partie 5 — Extension Graduate CSE 598 (Option B : Comportements générés) :**
  - Implémentation du générateur pseudo-aléatoire reproductible (`scripts/generate_driver_trace.py`).
  - Génération de 3 profils avec graines fixées (seeds 42, 101, 2024) dans `data/driver/`.
  - Exécution des simulations sous coach de règles : `results/extension-seed42`, `results/extension-seed101`, `results/extension-seed2024`.
  - Analyse comparative des métriques d'arrêt et des limites de validité.
- [x] **Livrables et archive de soumission officielle :**
  - Rédaction complète de `submission/answers.md` en anglais technique rigoureux.
  - Génération de l'archive ZIP via le script officiel `scripts/make_submission.py --groupid 01`.
  - Vérification de l'intégrité de l'archive (144 fichiers inclus, aucun fichier exclu ou artefact temporaire indésirable).

---

## 2. Commandes principales exécutées

```bash
# 1. Diagnostic environnement
python scripts/check_environment.py

# 2. Exemples Xronos
python examples/01_hello_reactor.py
python examples/02_timer_and_ports.py
python examples/03_logical_delay.py
python examples/04_deadline_lag.py
python examples/05_retroactive_fallback.py

# 3. Simulations déterministes de base
python -m agentic_driving_coach run --scenario stop-sign --driver beginner --coach rule --fast --output results/rule-a
python -m agentic_driving_coach run --scenario stop-sign --driver beginner --coach rule --fast --output results/rule-b
python -m agentic_driving_coach run --scenario stop-sign --driver beginner --coach replay --trace data/replay/example_trace.jsonl --fast --output results/replay
python -m agentic_driving_coach run --scenario stop-sign --driver beginner --coach rule --fast --output results/rule-deescalate

# 4. Évaluation modèles (traces de rejeu poste de travail)
python -m agentic_driving_coach run --scenario stop-sign --driver beginner --coach replay --trace data/replay/live_llama3.2-1b_300ms.jsonl --fast --output results/replay-1b-300
python -m agentic_driving_coach run --scenario stop-sign --driver beginner --coach replay --trace data/replay/live_llama3.2-3b_300ms.jsonl --fast --output results/replay-3b-300

# 5. Comparaison des profils de conduite
python -m agentic_driving_coach compare-behaviors --coach rule --drivers beginner advanced --repetitions 3 --fast --output results/behavior-comparison

# 6. Extension CSE 598 (génération et simulation)
python scripts/generate_driver_trace.py --seed 42 --output data/driver/generated_seed_42.txt
python scripts/generate_driver_trace.py --seed 101 --output data/driver/generated_seed_101.txt
python scripts/generate_driver_trace.py --seed 2024 --output data/driver/generated_seed_2024.txt
python -m agentic_driving_coach run --scenario stop-sign --driver data/driver/generated_seed_42.txt --coach rule --fast --output results/extension-seed42
python -m agentic_driving_coach run --scenario stop-sign --driver data/driver/generated_seed_101.txt --coach rule --fast --output results/extension-seed101
python -m agentic_driving_coach run --scenario stop-sign --driver data/driver/generated_seed_2024.txt --coach rule --fast --output results/extension-seed2024

# 7. Génération de l'archive officielle
python scripts/make_submission.py --groupid 01
```

---

## 3. Résultats importants

1. **Déterminisme temporel strict :**
   - Les simulations `rule-a` et `rule-b` produisent exactement les mêmes trajectoires physiques, décisions et métriques (`stopped=True`, `v_at_stop_line=0.0 m/s`, `stop_error=-4.522 m`). Seuls les horodatages réels et le lag système varient.
2. **Mécanisme d'armement et délais :**
   - Un décalage de 100 ms sépare la première décision `ACTUATE` (t=6700 ms, qui arme le Planner et donne un avertissement verbal) de l'émission effective du freinage d'urgence (t=6800 ms).
   - Un délai logique de 200 ms achemine l'actionnement jusqu'aux actionneurs du véhicule (application effective à t=7000 ms).
3. **Compromis Latence vs Qualité LLM :**
   - Avec une échéance stricte de 300 ms, `llama3.2:1b` a une latence médiane légèrement inférieure (349.8 ms vs 362.8 ms) et un taux de dépassement de 85.7% (contre 95.2% pour 3b), mais commet 1 faux négatif critique non sécurisé (`unsafe_false_negative=1`).
   - `llama3.2:3b` garantit zéro faux négatif non sécurisé, mais dépasse quasi-systématiquement l'échéance. Dans les deux cas, le dépassement de deadline dans la zone critique entraîne un dépassement de la ligne d'arrêt (+20 m).
4. **Impact du comportement conducteur :**
   - Le conducteur `advanced` freine plus tôt, réduisant le temps de violation de sécurité à 2.4 s (contre 3.1 s pour `beginner`) et ne nécessitant que 8 freinages d'urgence (contre 11 pour `beginner`), s'arrêtant 13.08 m avant la ligne (contre 4.52 m pour le débutant).

---

## 4. Limitations et remarques

- **Exécution locale sans GPU :** L'environnement d'exécution local sous WSL2 ne disposant pas de carte graphique dédiée ni d'instance Ollama active, l'évaluation des modèles a été réalisée avec les traces de rejeu certifiées fournies par le cours, conformément aux directives officielles de la section 3 du sujet.
- **Traces conducteurs en boucle ouverte :** Les traces de conduite générées ou enregistrées s'exécutent en boucle ouverte (le conducteur virtuel ne réagit pas aux conseils verbaux du coach).

---

## 5. Emplacement des livrables finaux

- **Fichier de réponses officiel :** `submission/answers.md`
- **Rapport d'environnement :** `results/environment.txt`
- **Générateur de traces (Extension CSE 598) :** `scripts/generate_driver_trace.py`
- **Traces générées :** `data/driver/generated_seed_42.txt`, `data/driver/generated_seed_101.txt`, `data/driver/generated_seed_2024.txt`
- **Dossiers de résultats complets :**
  - `results/rule-a/`
  - `results/rule-b/`
  - `results/replay/`
  - `results/rule-deescalate/`
  - `results/replay-1b-300/`
  - `results/replay-3b-300/`
  - `results/model-comparison/`
  - `results/behavior-comparison/`
  - `results/extension-seed42/`
  - `results/extension-seed101/`
  - `results/extension-seed2024/`
- **Archive ZIP officielle prête à soumettre :**
  `c:\Users\USER\Documents\my-agentic-driving-coach\submission\group01_agentic-driving-coach.zip`
