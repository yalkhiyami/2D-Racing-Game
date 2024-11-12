import pygame
pygame.font.init()
#source for imgscale: https://stackoverflow.com/questions/70819750/rotating-and-scaling-an-image-around-a-pivot-while-scaling-width-and-height-sep
def imgscale(img,factor):
    size = round(img.get_width()*factor), round (img.get_height()*factor)
    return pygame.transform.scale(img,size)
#https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame for screen fill and text
def rotatecenter(win,image,topleft,angle):
    rotatedimg = pygame.transform.rotate(image,angle)
    newrect = rotatedimg.get_rect(
        center=image.get_rect(topleft = topleft).center)
    win.blit(rotatedimg,newrect.topleft)
    
def centertext(win,font,text):
    render = font.render(text, 1, (0,0,0))
    win.blit(render,(win.get_width()/2-render.get_width()/2,win.get_height()/2-render.get_height()/2))
    
def titletext(win,font,text):
    render = font.render(text, 1, (200,200,200))
    win.blit(render,(win.get_width()/2-render.get_width()/2,win.get_height()/4-render.get_height()/2))
    
def subtitletext(win,font,text):
    render = font.render(text, 1, (200,200,200))
    win.blit(render,(win.get_width()/2-render.get_width()/2,win.get_height()/3-render.get_height()/2))


        
def subsubtitletext(win,font,text):
    render = font.render(text, 1, (0,200,200))
    win.blit(render,(win.get_width()/2-render.get_width()/2,win.get_height()/2 + 50 -render.get_height()/2))




