# MENGGERAKKAN ROBOT DENGAN ARROW [KIRI, KANAN, ATAS, BAWAH]
        # if varGlobals.keys_pressed[pygame.K_DOWN]:
        #     if dataRobot.xpos < varGlobals.res[1] - 1 and dataRobot.xpos <= 600:
        #         dataRobot.xpos += 1
        #         if dataRobot.xpos > 600:
        #             dataRobot.xpos = 600
        # if varGlobals.keys_pressed[pygame.K_UP]:
        #     if dataRobot.xpos > 0 and dataRobot.ypos <= 600:
        #         dataRobot.xpos -= 1
        #     if dataRobot.xpos > 0 and dataRobot.ypos > 600 and dataRobot.xpos > 200:
        #         dataRobot.xpos -= 1
        #         if dataRobot.xpos < 201:
        #             dataRobot.xpos = 201
        # if varGlobals.keys_pressed[pygame.K_LEFT]:
        #     if dataRobot.ypos > 0:
        #         dataRobot.ypos -= 1
        # if varGlobals.keys_pressed[pygame.K_RIGHT]:
        #     if dataRobot.ypos < varGlobals.res[0] - 1 and dataRobot.ypos <= 600 and dataRobot.xpos <= 200:
        #         dataRobot.ypos += 1
        #         if dataRobot.ypos > 600:
        #             dataRobot.ypos = 600
        #     elif dataRobot.ypos < varGlobals.res[0] - 1 and dataRobot.ypos <= 1000 and dataRobot.xpos > 200:
        #         dataRobot.ypos += 1
        #         if dataRobot.ypos > 1000:
        #             dataRobot.ypos = 1000
        # if varGlobals.keys_pressed[pygame.K_LSHIFT]:
        #     dataRobot.kompas += 1
        #     if dataRobot.kompas > 360:
        #         dataRobot.kompas = 0
        # if varGlobals.keys_pressed[pygame.K_LCTRL]:
        #     dataRobot.kompas -= 1
        #     if dataRobot.kompas < 0:
        #         dataRobot.kompas = 360