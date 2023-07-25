# Configurações iniciais
import pygame
import random
import button


def gerar_menu():
    pygame.init()
    larguraMenu, alturaMenu = 1200, 800
    telaMenu = pygame.display.set_mode((larguraMenu, alturaMenu))
    pygame.display.set_caption("Menu")

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        telaMenu.blit(img, (x, y))

    def desenhar_background(image):
        size = pygame.transform.scale(image, (1200, 800))
        telaMenu.blit(image, (0, 0))

    # variaveis
    failed = False

    font = pygame.font.SysFont("arialblack", 40)

    textColor = (255, 255, 255)

    background = pygame.image.load("images/menu.jpg")

    resume_img = pygame.image.load("images/button_resume.png")
    options_img = pygame.image.load("images/button_options.png")
    quit_img = pygame.image.load("images/button_quit.png")

    resume_button = button.Button(490, 360, resume_img, 1)
    # options_button = button.Button(470, 340, options_img, 1)
    quit_button = button.Button(490, 470, quit_img, 1)

    run = True
    while run:
        telaMenu.fill((0, 0, 0))
        desenhar_background(background)

        if failed == False:
            if resume_button.draw(telaMenu):
                failed = janela_jogo()
            if quit_button.draw(telaMenu):
                run = False
        elif failed == "sair":
            run = False
        else:
            draw_text(
                "Você perdeu, aperte espaço para ir pro menu!",
                font,
                textColor,
                100,
                380,
            )

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    failed = False
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


def janela_jogo():
    pygame.init()
    pygame.display.set_caption("Jogo da Cobrinha Python")
    largura, altura = 1200, 800
    tela = pygame.display.set_mode((largura, altura))
    relogio = pygame.time.Clock()

    # Cores - RGB
    preta = (0, 0, 0)
    branca = (255, 255, 255)
    vermelha = (255, 0, 0)
    verde = (0, 225, 0)
    azul = (0, 0, 255)

    # Parâmetros da cobrinha
    tamanho_do_quadrado = 20

    def gerar_comida():
        comida_x = round(
            random.randrange(0, largura - tamanho_do_quadrado)
            / float(tamanho_do_quadrado)
        ) * float(tamanho_do_quadrado)
        comida_y = round(
            random.randrange(0, altura - tamanho_do_quadrado)
            / float(tamanho_do_quadrado)
        ) * float(tamanho_do_quadrado)
        return comida_x, comida_y

    def desenhar_comida(tamanho, comida_x, comida_y):
        pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

    def desenhar_acelerador(tamanho, acelerador_x, acelerador_y):
        pygame.draw.rect(tela, azul, [acelerador_x, acelerador_y, tamanho, tamanho])

    def desenhar_cobra(tamanho, pixels):
        for pixel in pixels:
            pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

    def desenhar_pontuacao(pontuacao):
        fonte = pygame.font.SysFont("Helvetica", 25)
        texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
        tela.blit(texto, [1, 1])

    def selecionar_velocidade(tecla):
        if tecla == pygame.K_DOWN:
            velocidade_x = 0
            velocidade_y = tamanho_do_quadrado
        elif tecla == pygame.K_UP:
            velocidade_x = 0
            velocidade_y = -tamanho_do_quadrado
        elif tecla == pygame.K_RIGHT:
            velocidade_x = tamanho_do_quadrado
            velocidade_y = 0
        elif tecla == pygame.K_LEFT:
            velocidade_x = -tamanho_do_quadrado
            velocidade_y = 0
        return velocidade_x, velocidade_y

    def rodar_jogo():
        velocidade_jogo = 15
        fim_jogo = False
        x = largura / 2
        y = altura / 2

        velocidade_x = 0
        velocidade_y = 0

        tamanho_cobra = 1
        pixels = []

        comida_x, comida_y = gerar_comida()
        acelerador_x, acelerador_y = gerar_comida()
        intervalo_acelerador = 15000
        tempo_anterior = pygame.time.get_ticks()
        direcao_atual_x = 0
        direcao_atual_y = 0

        while not fim_jogo:
            tela.fill(preta)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    fim_jogo = True
                elif evento.type == pygame.KEYDOWN:
                    # Verifica se a direção solicitada não é a oposta da direção atual
                    if (
                        evento.key == pygame.K_DOWN
                        and direcao_atual_y != -tamanho_do_quadrado
                    ):
                        direcao_atual_x, direcao_atual_y = selecionar_velocidade(
                            evento.key
                        )
                    elif (
                        evento.key == pygame.K_UP
                        and direcao_atual_y != tamanho_do_quadrado
                    ):
                        direcao_atual_x, direcao_atual_y = selecionar_velocidade(
                            evento.key
                        )
                    elif (
                        evento.key == pygame.K_RIGHT
                        and direcao_atual_x != -tamanho_do_quadrado
                    ):
                        direcao_atual_x, direcao_atual_y = selecionar_velocidade(
                            evento.key
                        )
                    elif (
                        evento.key == pygame.K_LEFT
                        and direcao_atual_x != tamanho_do_quadrado
                    ):
                        direcao_atual_x, direcao_atual_y = selecionar_velocidade(
                            evento.key
                        )

            # atualizar a posição da cobra
            if x < 0 or x >= largura or y < 0 or y >= altura:
                fim_jogo = True
                return True

            x += direcao_atual_x
            y += direcao_atual_y

            proximo_tempo = pygame.time.get_ticks()
            if proximo_tempo - tempo_anterior >= intervalo_acelerador:
                # desenha o acelerador
                desenhar_acelerador(tamanho_do_quadrado, acelerador_x, acelerador_y)

            # desenha a comida
            desenhar_comida(tamanho_do_quadrado, comida_x, comida_y)

            # desenha a cobra
            pixels.append([x, y])
            if len(pixels) > tamanho_cobra:
                del pixels[0]

            # Verifica se a cobra bateu no corpo
            for pixel in pixels[:-1]:
                if pixel == [x, y]:
                    fim_jogo = True
                    return True
            desenhar_cobra(tamanho_do_quadrado, pixels)
            # desenha os pontos
            desenhar_pontuacao(tamanho_cobra - 1)

            # Atualização da tela
            pygame.display.update()

            # Criar uma nova comida
            if x == comida_x and y == comida_y:
                tamanho_cobra += 1
                comida_x, comida_y = gerar_comida()

            if "acelerador_x" in locals() and "acelerador_y" in locals():
                if x == acelerador_x and y == acelerador_y:
                    tempo_anterior = proximo_tempo
                    acelerador_x, acelerador_y = gerar_comida()
                    velocidade_antes = velocidade_jogo
                    velocidade_jogo = velocidade_antes + 1
                relogio.tick(velocidade_jogo)
            else:
                relogio.tick(velocidade_jogo)
        return True

    rodar_jogo()


gerar_menu()
