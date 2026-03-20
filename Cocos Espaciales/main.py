#pgzero
import random

WIDTH = 600
HEIGHT = 450

TITLE = "COCOS COSMICOS"
FPS = 30
ship = Actor("ship", (300, 400))
space = Actor("space")
tipo1 = Actor("ship1", (100, 200))
tipo2 = Actor("ship2", (300, 200))
tipo3 = Actor("ship3", (500, 200))

score = 0
survival_timer = 0

enemies = []
planets = [
    Actor("plan1", (random.randint(0, 600), -100)),
    Actor("plan2", (random.randint(0, 600), -100)),
    Actor("plan3", (random.randint(0, 600), -100))
]
meteors = []
mode = 'menu'
bullets = []

for i in range(5):
    x = random.randint(0, 600)
    y = random.randint(-450, -50)
    enemy = Actor("coconu", (x, y))
    enemy.speed = random.randint(2, 8)
    enemies.append(enemy)

for i in range(5):
    x = random.randint(0, 600)
    y = random.randint(-450, -50)
    meteor = Actor("meteor", (x, y))
    meteor.speed = random.randint(2, 10)
    meteors.append(meteor)

def draw():
    if mode == "menu":
        space.draw()
        screen.draw.text('ELIGE TU NAVE', center=(300, 100), color="white", fontsize=36)
        screen.draw.text("COCOS COSMICOS", center=(300, 400), color="white", fontsize=50)
        tipo1.draw()
        tipo2.draw()
        tipo3.draw()

    elif mode == "game":
        space.draw()
        for planet_obj in planets:
            planet_obj.draw()
        for meteor in meteors:
            meteor.draw()
        ship.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()

        screen.draw.text("SCORE: " + str(score), center=(80, 20), fontsize=30, color="white")

    elif mode == "end":
        space.draw()
        screen.draw.text("TE COCARON LOS COCOS", center=(300, 200), color="white", fontsize=36)
        screen.draw.text("Presiona R para reiniciar", center=(300, 250), color="white", fontsize=24)

def on_mouse_move(pos):
    ship.pos = pos

def new_enemy():
    x = random.randint(0, 400)
    y = -50
    enemy = Actor("coconu", (x, y))
    enemy.speed = random.randint(2, 8)
    enemies.append(enemy)

def enemy_coconu():
    for enemy in enemies[:]:
        enemy.y += enemy.speed
        if enemy.y > HEIGHT + 50:
            enemies.remove(enemy)
            new_enemy()

def planet():
    global score
    if planets[0].y < 550:
        planets[0].y += 1
    else:
        score += 150
        planets[0].y = -100
        planets[0].x = random.randint(0, 600)
        first = planets.pop(0)
        planets.append(first)

def meteorites():
    for meteor in meteors:
        if meteor.y < HEIGHT:
            meteor.y += meteor.speed
        else:
            meteor.x = random.randint(0, WIDTH)
            meteor.y = -20
            meteor.speed = random.randint(2, 10)

def collisions():
    global mode, score

    for enemy in enemies[:]:
        if ship.colliderect(enemy):
            mode = 'end'
            return
        for bullet in bullets[:]:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                new_enemy()
                score += 25
                return

    for meteor in meteors:
        if ship.colliderect(meteor):
            mode = 'end'
            return

    for planet_obj in planets:
        if ship.colliderect(planet_obj):
            mode = 'end'
            return

def restart_game():
    global enemies, meteors, bullets, planets, mode, ship, score, survival_timer

    score = 0
    survival_timer = 0
    ship.pos = (300, 400)
    bullets = []

    enemies = []
    for i in range(5):
        x = random.randint(0, 600)
        y = random.randint(-450, -50)
        enemy = Actor("coconu", (x, y))
        enemy.speed = random.randint(2, 8)
        enemies.append(enemy)

    meteors = []
    for i in range(5):
        x = random.randint(0, 600)
        y = random.randint(-450, -50)
        meteor = Actor("meteor", (x, y))
        meteor.speed = random.randint(2, 10)
        meteors.append(meteor)

    planets = [
        Actor("plan1", (random.randint(0, 600), -100)),
        Actor("plan2", (random.randint(0, 600), -100)),
        Actor("plan3", (random.randint(0, 600), -100))
    ]

    mode = "menu"

def update(dt):
    global survival_timer, score

    if mode == 'game':
        enemy_coconu()
        collisions()
        planet()
        meteorites()

        for bullet in bullets[:]:
            if bullet.y < 0:
                bullets.remove(bullet)
            else:
                bullet.y -= 10

        survival_timer += dt
        if survival_timer >= 10:
            score += 50
            survival_timer = 0

def on_mouse_down(button, pos):
    global mode, ship
    if mode == "menu" and tipo1.collidepoint(pos):
        ship.image = "ship1"
        mode = "game"

    if mode == "menu" and tipo3.collidepoint(pos):
        ship.image = "ship3"
        mode = "game"

    if mode == "menu" and tipo2.collidepoint(pos):
        ship.image = "ship2"
        mode = "game"

    if mode == "game" and button == mouse.LEFT:
        num_bullets = score // 1000
        if num_bullets > 4:
            num_bullets = 4
        if num_bullets < 1:
            num_bullets = 1

        spread = 30
        center = (num_bullets - 1) // 2

        for i in range(num_bullets):
            offset = (i - center) * spread
            bullet = Actor("missiles")  # Replace with valid image if needed
            bullet.pos = (ship.x + offset, ship.y)
            bullets.append(bullet)
            print("Bullet created at offset:", offset)

def on_key_down(key):
    global mode
    if mode == "end" and key == keys.R:
        restart_game()
