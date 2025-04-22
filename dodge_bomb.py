import os
import time
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650 

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：判定結果タプル（横, 縦）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True  # 横, 縦方向用の変数
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right:  #　画面外だったら
        yoko = False
    #縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:   #　画面外だったら
        tate = False
    return yoko, tate

    #　ゲームオーバー画面  
def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバーの画面設定
    薄黒いバックグラウンド
    泣きこうかとん
    Game Over 文字
    """
    sika = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(sika, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT)) #黒画面　大きさ
    sika.set_alpha(200) #黒濃さ 
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255)) #文字と色
    txt_rct = txt.get_rect()
    #薄黒画面の中心座標2行↓
    txt_rct.centerx = WIDTH/2
    txt_rct.centery = HEIGHT/2
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk2_rct = kk2_img.get_rect()
    kk2_rct.center = 350, HEIGHT   #泣きこうかとん左
    screen.blit(sika, [0, 0])      # 薄黒画面の座標
    screen.blit(kk2_img, kk2_rct)
    kk2_rct.center = 750, HEIGHT/2 #泣きこうかとん右
    screen.blit(kk2_img, kk2_rct)
    screen.blit(txt, txt_rct)
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # こうかとん元気初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #こうかとん悲しい初期化
  
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk2_rct = kk2_img.get_rect()
    kk2_rct.center = 300, 200

    #　 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5


    clock = pg.time.Clock()
    tmr = 0
  
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        #　こうかとんrectと爆弾rectが重なっていあたら
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            gameover(screen)
            return


        key_lst = pg.key.get_pressed()

        DELTA = {
            pg.K_UP: (0,-5),
            pg.K_DOWN: (0,+5),
            pg.K_LEFT: (-5,-0),
            pg.K_RIGHT: (+5,-0),
        }
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #左右方向
                sum_mv[1] += mv[1]  #上下方向

        
        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #画面内に戻す
        screen.blit(kk_img, kk_rct) #こうかとんの描画
        bb_rct.move_ip(vx, vy)  #爆発の移動
        yoko, tate =check_bound(bb_rct)
        if not yoko:  #左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  #上下どちらかにはみ出ていたら
            vy *= -1


        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
