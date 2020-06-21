import configparser
import pygame
class SimpleTetrisConfig():
    configFilePath = './config.ini'
    
    #default config
    
    #Key
    key_Left = pygame.K_a
    key_Right = pygame.K_d
    key_SoftDrop = pygame.K_s
    key_HardDrop = pygame.K_SPACE
    key_SpinCW = pygame.K_j
    key_SpinCCW = pygame.K_l
    key_Hold = pygame.K_k
    
    #Network
    nickname = 'noname'
    server_ip = '127.0.0.1'
    
    def __init__(self):
        self.loadConfig()
        
    def loadConfig(self):
        print('Reading', self.configFilePath, '...')
        
        config = configparser.RawConfigParser()
        
        try:
            config.read_file(open(self.configFilePath, 'r'))
            
            self.key_Left = config.getint('Key', 'left')
            self.key_Right = config.getint('Key', 'right')
            self.key_SoftDrop = config.getint('Key', 'softdrop')
            self.key_HardDrop = config.getint('Key', 'hardrop')
            self.key_SpinCW = config.getint('Key', 'spincw')
            self.key_SpinCCW = config.getint('Key', 'spinccw')
            self.key_Hold = config.getint('Key', 'hold')
            self.nickname = config.get('Network', 'nickname')
            self.server_ip = config.get('Network', 'server_ip')
            
        except BaseException:
            print('Fail to load config file. Fixing config file...')
            self.writeConfig()
            
        print('Reading done.')
    
    def writeConfig(self):
        print('Writing config file...')
        config = configparser.RawConfigParser()
        
        config.add_section('Key')
        config.set('Key', 'left', self.key_Left)
        config.set('Key', 'right', self.key_Right)
        config.set('Key', 'softdrop', self.key_SoftDrop)
        config.set('Key', 'hardrop', self.key_HardDrop)
        config.set('Key', 'spincw', self.key_SpinCW)
        config.set('Key', 'spinccw', self.key_SpinCCW)
        config.set('Key', 'hold', self.key_Hold)
        
        config.add_section('Network')
        config.set('Network', 'nickname', self.nickname)
        config.set('Network', 'server_ip', self.server_ip)
        
        try:
            with open(self.configFilePath, 'w') as configFile:
                config.write(configFile)
                configFile.close()
        except:
            raise
        
        print('Writing done.')