# Makefile para el Proyecto de Buscador de Documentos
# Directorios
DATA_RAW := data/raw
DATA_DOCS := data/docs
INDEX_RAW := index/raw
INDEX_CLEAN := index/clean
SRC := src

# Archivos
CSV_TO_TXT := $(SRC)/csv_to_txt.py
BUILD_AWK := $(SRC)/build_index.awk
REMOVER_PY := $(SRC)/stopword_remover.py
BUSCADOR_PY := $(SRC)/buscador.py

.PHONY: all clean index clean_index search docs

all: docs index clean_index search
	@echo "--------------------------------------------------------"
	@echo "Proyecto de Buscador finalizado. Ejecute 'make search' para probar."
	@echo "--------------------------------------------------------"

# 1. Preparar Documentos
docs: $(DATA_DOCS)
	@echo "--- 1. Preparando documentos desde CSV ---"
	python3 $(CSV_TO_TXT)

# 2. Construir el Índice Bruto 
index: $(INDEX_RAW)
	@echo "--- 2. Construyendo índice bruto con AWK ---"
	# Ejecuta AWK sobre todos los documentos .txt
	awk -v OUTDIR="$(INDEX_RAW)" -f $(BUILD_AWK) $(DATA_DOCS)/*.txt

# 3. Limpiar Stopwords
clean_index: $(INDEX_CLEAN)
	@echo "--- 3. Limpiando stopwords del índice ---"
	python3 $(REMOVER_PY) # <--- ¡IMPORTANTE! python3 en WSL

# 4. Iniciar el Buscador 
search:
	@echo "--- 4. Iniciando Buscador ---"
	python3 $(BUSCADOR_PY) # <--- ¡IMPORTANTE! python3 en WSL

# Creación de directorios necesarios
$(DATA_DOCS) $(INDEX_RAW) $(INDEX_CLEAN):
	mkdir -p $@

# Limpieza general
clean:
	@echo "--- Limpiando archivos generados ---"
	rm -rf $(DATA_DOCS)
	rm -rf $(INDEX_RAW)
	rm -rf $(INDEX_CLEAN)