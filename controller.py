import pygame

class GameController:
    def __init__(self, world, renderer, hotbar=None):
        self.world = world
        self.renderer = renderer
        self.hotbar = hotbar
        self.running = True

    def process_input(self):
        """Reads keyboard input and returns movement flags."""
        keys = pygame.key.get_pressed()

        left  = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        jump  = keys[pygame.K_SPACE]

        # Hotbar selection (1–9)
        if self.hotbar:
            for i, key in enumerate([
                pygame.K_1, pygame.K_2, pygame.K_3,
                pygame.K_4, pygame.K_5, pygame.K_6,
                pygame.K_7, pygame.K_8, pygame.K_9
            ]):
                if keys[key]:
                    self.hotbar.selected_slot = i
                    break

        return left, right, jump

    def process_events(self):
        """Handles quit events and ESC key."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Main per-frame update: input → collisions → model → view."""
        self.process_events()
        if not self.running:
            return False

        # 1. Read input
        left, right, jump = self.process_input()

        # 2. Get pixel-perfect collision hits from the VIEW
        mask_hits = self.renderer.get_collision_hits()

        # 3. Update the MODEL
        self.world.update(left, right, jump, mask_hits)

        # 4. Handle interactables
        self.handle_interactions()

        # 5. Draw everything
        self.renderer.draw()
        pygame.display.update()

        return True

    def handle_interactions(self):
        """Checks if the player is touching interactables and handles logic."""
        player = self.world.player

        for inter in self.world.interactables:
            if not inter.visible:
                continue

            # Simple AABB check (mask collision is handled in view)
            px, py = player.pos
            pw, ph = player.size
            ix, iy = inter.pos
            iw, ih = inter.size

            if (px < ix + iw and px + pw > ix and
                py < iy + ih and py + ph > iy):

                held_item = None
                if self.hotbar:
                    held_item = self.hotbar.hotbar[self.hotbar.selected_slot]

                end_triggered = inter.interact(held_item)

                if end_triggered:
                    print("END GAME TRIGGERED")
                    self.running = False
