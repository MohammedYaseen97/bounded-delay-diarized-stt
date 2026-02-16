.PHONY: test check-week0 check-week1 check-week2 check-week3 check-week4 check-week5 check-week6

test:
	python -m pytest -q

check-week0:
	python scripts/check_week0.py

check-week1:
	python scripts/check_week1_offline_e2e.py

check-week2:
	python scripts/check_week2_vad_and_tracking.py

check-week3:
	python scripts/check_week3_stabilizer.py

check-week4:
	python scripts/check_week4_streaming_semantics.py

check-week5:
	bash scripts/check_week5_packaging.sh

check-week6:
	python scripts/check_week6_report_artifacts.py

