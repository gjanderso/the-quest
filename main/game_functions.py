import sys, pygame
import characters


def check_events(player, mobs):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_q:
                player.use_weapon()
            elif event.key == pygame.K_v:
                player.weapon.toggled = not player.weapon.toggled

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_LEFT:
                player.moving_left = False


def update_mobs(game_settings, screen, mobs, player):
    # Adding mobs
    if len(mobs) == 0:
        mobs.add(characters.Imp(game_settings, screen))

    # Updating mobs
    for mob in mobs.sprites():
        mob.check_collision(player)
        mob.update(player)
    #mobs.update(player)

    for mob in mobs.copy():
        if mob.rect.right <= 0:
            mobs.remove(mob)


def update_screen(game_settings, screen, clock, forrest, player, mobs):

    screen.fill(game_settings.bg_color)

    forrest.blitme()
    player.blitme()
    for mob in mobs.sprites():
        mob.blitme()

    if player.hp <= 0:
        print('Game Over')
        sys.exit()

    pygame.display.flip()
    clock.tick(game_settings.fps)
