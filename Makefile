.PHONY: run test gun stats clean
run:   ; python3 life.py
test:  ; python3 -m unittest -v
gun:   ; python3 life.py --pattern glider_gun --width 50 --height 30
stats: ; python3 stats.py --pattern glider_gun --generations 400
clean: ; rm -rf __pycache__ *.html
