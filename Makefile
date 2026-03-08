IMAGE=hexaexam/wordpress:latest

.PHONY: build up down ps logs save load push clean reset

build:
	docker-compose build --no-cache wordpress

up: build
	docker-compose up -d
	@echo ""
	@echo "============================================"
	@echo "  HexaDynamics Lab Starting..."
	@echo "  Wait ~60 seconds for full setup."
	@echo ""
	@echo "  Corporate site: http://localhost:8080"
	@echo "  WordPress:      http://localhost:8080/intranet"
	@echo "  SSH:            ssh marketing@localhost -p 2222"
	@echo "============================================"

down:
	docker-compose down

clean:
	docker-compose down -v
	docker rmi $(IMAGE) 2>/dev/null || true

reset: clean up

ps:
	docker-compose ps

logs:
	docker logs hs_wp_web --tail 200

save:
	@echo "Saving image $(IMAGE) to hexaexam-wordpress.tar"
	docker save -o hexaexam-wordpress.tar $(IMAGE)

load:
	@echo "Loading image from hexaexam-wordpress.tar"
	docker load -i hexaexam-wordpress.tar

push:
	@echo "Tagging and pushing $(IMAGE) to registry (ensure you're logged in)"
	docker push $(IMAGE)
