PYTHONPATH=../src/ MISSING_RATE=0.3 python -m train --bmname=ENZYMES --assign-ratio=0.1 --hidden-dim=30 --output-dim=30 --cuda=0 --num-classes=6 --method=soft-assign --epochs 100
