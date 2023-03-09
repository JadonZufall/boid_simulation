import math
import numpy as np

import pygame
pygame.init()

# Constants
WIN_W: int = 2_000
WIN_H: int = 1_000

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)

# Globals
window: pygame.Surface = pygame.display.set_mode((WIN_W, WIN_H), flags=0, depth=0, display=0, vsync=1)
clock: pygame.time.Clock = pygame.time.Clock()

img_mem: list[pygame.Surface] = []
font = pygame.font.SysFont("Arial", 24)

entity = list[float, float, float, float, int]
# 0 = xpos, 1 = ypos, 2 = vel, 3 = rot, 4 = imgindex, 5 = activeSurface
entities: list[entity] = []

HOSTILE_WIDTH: int = 5
HOSTILE_SCALE: tuple[int, int] = (50, 50)
hostile_ship: pygame.Surface = pygame.Surface(HOSTILE_SCALE, pygame.SRCALPHA)
HOSTILE_POLYGON: list[tuple[int, int]] = [
    (HOSTILE_SCALE[0] // 2 + 1, 0),
    (HOSTILE_SCALE[0], HOSTILE_SCALE[1]),
    (HOSTILE_SCALE[0] // 2 + 1, int(HOSTILE_SCALE[1] * 0.80)),
    (0, HOSTILE_SCALE[1]),
    (HOSTILE_SCALE[0] // 2 + 1, 0),
]
pygame.draw.polygon(hostile_ship, (255, 0, 0), HOSTILE_POLYGON, HOSTILE_WIDTH)
img_mem.append(hostile_ship)


def spawn_entity(x: float, y: float, vel: float, rot: float, img: int) -> int:
    global entities
    ent: entity = [x, y, vel, rot, img]
    entities.append(ent)
    return len(entities) - 1


def spawn_enemy(x: float, y: float, vel: float, rot: float) -> int:
    return spawn_entity(x, y, vel, rot, 0)


# Generated Graphics
PLAYER_WIDTH: int = 5
PLAYER_SCALE: tuple[int, int] = (50, 50)
spaceship: pygame.Surface = pygame.Surface(PLAYER_SCALE, pygame.SRCALPHA)
PLAYER_POLYGON: list[tuple[int, int]] = [
    (PLAYER_SCALE[0] // 2 + 1, 0),
    (PLAYER_SCALE[0], PLAYER_SCALE[1]),
    (PLAYER_SCALE[0] // 2 + 1, int(PLAYER_SCALE[1] * 0.80)),
    (0, PLAYER_SCALE[1]),
    (PLAYER_SCALE[0] // 2 + 1, 0),
]
pygame.draw.polygon(spaceship, BLACK, PLAYER_POLYGON, width=PLAYER_WIDTH)
player_spaceship: pygame.Surface = pygame.Surface(PLAYER_SCALE, pygame.SRCALPHA)
player_spaceship.blit(spaceship, (0, 0))


# Global state values
is_running: bool = False
is_paused: int = False

debounce: list[bool] = [False for i in range(0, 1000)]


# Camera state
camera_x: float = 0.0
camera_y: float = 0.0


# Player state
player_x: float = WIN_W / 2
player_y: float = WIN_H / 2
player_rot: float = -90
player_vel: float = 0.0


player_spaceship = pygame.transform.rotate(player_spaceship, player_rot)


def calculate_center_point(position: tuple[float, float], size: tuple[int, int]) -> tuple[float, float]:
    center_x: float = position[0] - (size[0] / 2)
    center_y: float = position[1] - (size[1] / 2)
    return center_x, center_y


def calculate_rotation(terminal_point: tuple[float, float], initial_point: tuple[float, float]) -> float:
    delta_x = terminal_point[0] - initial_point[0]
    delta_y = terminal_point[1] - initial_point[1]
    return np.arctan2(delta_x, delta_y)


def calculate_rotational_velocity(rotation: float, velocity: float) -> tuple[float, float]:
    velocity_x: float = np.cos(rotation) * velocity
    velocity_y: float = np.sin(rotation) * velocity
    return velocity_x, velocity_y


def calculate_magnitude(terminal_point: tuple[float, float], initial_point: tuple[float, float]) -> tuple[float, float]:
    delta_x = terminal_point[0] - initial_point[0]
    delta_y = terminal_point[1] - initial_point[1]
    return np.sqrt(np.square(delta_x) + np.square(delta_y))


def normalize_vector(terminal_point: tuple[float, float], initial_point: tuple[float, float]) -> tuple[float, float]:
    delta_x = terminal_point[0] - initial_point[0]
    delta_y = terminal_point[1] - initial_point[1]
    magnitude: float = np.sqrt(np.square(delta_x) + np.square(delta_y))
    if magnitude == 0:
        return 0, 0
    return delta_x / magnitude, delta_y / magnitude


def apply_camera_offset(target_point: tuple[float, float]) -> None:
    offset_x: float = target_point[0] - camera_x
    offset_y: float = target_point[1] - camera_y
    return offset_x, offset_y


def center_camera(target_point: tuple[float, float]) -> tuple[float, float]:
    offset_x: float = target_point[0] - WIN_W / 2
    offset_y: float = target_point[1] - WIN_H / 2
    return offset_x, offset_y



if __name__ == "__main__":
    is_running = True


while is_running:
    clock.tick(60)
    dt: float = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        if not debounce[pygame.K_o]:
            print("PAUSED")
            is_paused = not is_paused
        debounce[pygame.K_o] = True
    else:
        debounce[pygame.K_o] = False

    if is_paused:
        pygame.display.set_caption("PAUSED")
        continue

    if keys[pygame.K_w]:
        player_vel += 100 * dt
    if keys[pygame.K_s]:
        player_vel -= 100 * dt
    if keys[pygame.K_a]:
        player_rot += 1
        player_spaceship = pygame.transform.rotate(spaceship, player_rot)
    if keys[pygame.K_d]:
        player_rot -= 1
        player_spaceship = pygame.transform.rotate(spaceship, player_rot)
    
    """
    if keys[pygame.K_UP]:
        camera_y -= 1
    if keys[pygame.K_DOWN]:
        camera_y += 1
    if keys[pygame.K_LEFT]:
        camera_x -= 1
    if keys[pygame.K_RIGHT]:
        camera_x += 1
    """

    camera_x, camera_y = center_camera((player_x, player_y))

    if keys[pygame.K_p]:
        if not debounce[pygame.K_p]:
            debounce[pygame.K_p] = True
            spawn_enemy(player_x, player_y, player_vel, player_rot)
    else:
        debounce[pygame.K_p] = False
    
    if keys[pygame.K_i]:
        # For stress testing remove later.
        spawn_enemy(player_x - 10, player_y - 10, player_vel - 10, player_rot)
    

    window.fill(WHITE)
    
    for index, ent in enumerate(entities):
        delta_y, delta_x = calculate_rotational_velocity(np.deg2rad(ent[3]), ent[2])
        delta_y, delta_x = -1 * delta_y * dt, -1 * delta_x * dt

        mag_before = calculate_magnitude((ent[0], ent[1]), (player_x, player_y))
        entities[index][0] += delta_x
        entities[index][1] += delta_y
        mag_after = calculate_magnitude((entities[index][0], entities[index][1]), (player_x, player_y))

        for i, e in enumerate(entities):
            e_mag = calculate_magnitude((entities[index][0], entities[index][1]), (e[0], e[1]))
            v_mod = entities[index][3]
            if e_mag < 50:
                entities[index][3] = -entities[index][3]
            entities[i][3] += v_mod
            break

        if mag_before > 50:
            if mag_before < mag_after:
                entities[index][2] -= 75 * dt
            else:
                entities[index][2] += 75 * dt
        else:
            entities[index][2] = entities[index][2] * 0.90

        img = pygame.transform.rotate(img_mem[ent[4]], ent[3])
        window.blit(img, apply_camera_offset(calculate_center_point((ent[0], ent[1]), img.get_size())))

        deg_diff = entities[index][3] - np.rad2deg(calculate_rotation((ent[0], ent[1]), (player_x, player_y)))
        deg_diff = deg_diff * 0.1
        entities[index][3] -= deg_diff

    delta_y, delta_x = calculate_rotational_velocity(np.deg2rad(player_rot), player_vel)
    delta_y, delta_x = -1 * delta_y * dt, -1 * delta_x * dt
    pygame.display.set_caption(f"{delta_x}, {delta_y}")
    player_x += delta_x
    player_y += delta_y
    
    player_center_point = calculate_center_point((player_x, player_y), player_spaceship.get_size())
    window.blit(player_spaceship, apply_camera_offset(calculate_center_point((player_x, player_y), player_spaceship.get_size())))
    pygame.draw.line(window, (255, 0, 0), apply_camera_offset((player_x, player_y)), apply_camera_offset((player_x + delta_x * 10, player_y + delta_y * 10)))
    txt0 = font.render(f"FPS {clock.get_fps()}", True, BLACK)
    txt1 = font.render(f"ENTITY_COUNT {len(entities)}", True, BLACK)
    window.blit(txt0, (50, 50))
    window.blit(txt1, (50, 100))
    pygame.display.flip()



