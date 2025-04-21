# Inclusion des fichiers d'environnement s'ils existent
ifneq (,$(wildcard dotenv/*.env))
    include dotenv/*.env
    export
endif

# Définition des fichiers Docker Compose
COMPOSE_FILES := -f compose.local.yaml

# Objectif par défaut
.DEFAULT_GOAL := help

# Couleurs pour l'affichage de l'aide
COLOR_TARGET := \033[36m
COLOR_DESC := \033[0m

# Cibles phony
.PHONY: help run restart stop logs down prune volume pre-commit

# Affiche l'aide avec les descriptions des cibles
help: ## Afficher cette aide
	@echo "Cibles disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(COLOR_TARGET)%-30s$(COLOR_DESC)%s\n", $$1, $$2}'


# Exécute les conteneurs
run: ## Démarrer les conteneurs
	docker compose $(COMPOSE_FILES) up

# Redémarre un ou plusieurs conteneurs
restart: ## Redémarrer un ou plusieurs conteneurs (utiliser SERVICE=<service>)
	docker compose $(COMPOSE_FILES) restart $(SERVICE)

# Arrête un ou tous les conteneurs
stop: ## Arrêter un ou tous les conteneurs (utiliser SERVICE=<service>)
	docker compose $(COMPOSE_FILES) stop $(SERVICE)

# Affiche les logs des conteneurs
logs: ## Voir les logs des conteneurs (utiliser SERVICE=<service>)
	docker compose $(COMPOSE_FILES) logs -f $(SERVICE)

# Supprime les conteneurs, réseaux, etc.
down: ## Arrêter les services et supprimer les conteneurs, réseaux, volumes
	docker compose $(COMPOSE_FILES) down

# Nettoie les ressources Docker non utilisées
prune: ## Nettoyer les images, conteneurs et réseaux non utilisés
	docker system prune

# Nettoie les volumes Docker non utilisés
volume: ## Nettoyer les volumes Docker non utilisés
	docker volume prune

.PHONY: tests
tests: ## Execute test
	poetry run coverage run -m pytest -vvv tests

.PHONY: coverage
coverage: ## Execute coverage
	poetry run coverage report -m

# Exécute les hooks de pré-commit
pre-commit: ## Exécuter les hooks de pré-commit
	pre-commit run --all-files
