import sys
import ast
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageOps

# puzzle should be in main.py

class ShowPuzzle:
    def __init__(self, puzzle, solution):
        self.puzzle = puzzle
        self.current_position = puzzle.copy()
        self.solution = solution
        self.x = [0] * 9
        self.y = [0] * 9
        self.moving_sq = None
        self.dx = 0.0
        self.dy = 0.0
        self.move_counter = 0
        self.solved = False
        self.solve_time = 75.0
        self.text = [0] * 8

    def main(self):

        # initに引数を渡す
        glutInit(sys.argv)

        # 表示モードの種類を選択
        # Double buffer, RGBA color, アルファコンポーネント対応 Depth buffer
        glutInitDisplayMode(GLUT_SINGLE, GLUT_RGBA)
        
        # ウィンドウを初期化
        glutInitWindowSize(500, 500)
        
        # ウィンドウの座標の初期化、画面の左上隅
        glutInitWindowPosition(500, 0)
        
        # 閉じるときに使用するウィンドウIDを保持
        window = glutCreateWindow("8Puzzle!".encode("cp932"))

        # glutで描画関数を登録    
        glutDisplayFunc(self.DrawGLScene)
        
        # この行のコメントを外すとフルスクリーンになる
        #glutFullScreen()

        # 何もしていないとき、シーンの再描画
        glutIdleFunc(self.DrawGLScene)

        # ウィンドウのサイズ変更時に呼び出される関数を登録
        glutReshapeFunc(self.ReSizeGLScene)
        
        # キーボードが押されたときに呼び出される関数を登録
        glutKeyboardFunc(self.keyPressed)

        # GLの初期化
        self.InitGL(500, 500)

        # MainLoopを実行
        glutMainLoop()

    def LoadTextures(self, n):
        #global texture
        name = "archive/num/" + str(n) + ".bmp"
        image = Image.open(name)
        image = ImageOps.flip(image)
        ix, iy = image.size
        image = image.tobytes()
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1)) 
        
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


    def solve(self):

        # global solution, current_position, moving_sq, x, y, dx, dy, move_counter, solved, solve_time
        # print(current_position)
        if len(self.solution) == 1:
            self.solved = True
            return None

        if self.moving_sq == None:
            for j in range(len(self.current_position)):
                if self.current_position[j] == self.solution[1]:
                    self.moving_sq = j
                    cory_tar, corx_tar = self.solution[1]
                    cory_0, corx_0 = self.solution[0]
                    self.dx = 1.2*(corx_tar - corx_0) / self.solve_time
                    self.dy = 1.2*(cory_tar - cory_0) / self.solve_time
                    self.move_counter += 1
                    self.x[self.moving_sq] -= self.dx
                    self.y[self.moving_sq] += self.dy
        else:
            # if square finishes moving
            if self.move_counter == self.solve_time:
                # Initialize
                self.current_position[0], self.current_position[self.moving_sq] = self.current_position[self.moving_sq], self.current_position[0]
                self.moving_sq = None
                self.move_counter = 0
                # print(current_position)
                # move to next step
                del(self.solution[0])
                if len(self.solution) == 1:
                    self.solved = True
            else:
                self.x[self.moving_sq] -= self.dx
                self.y[self.moving_sq] += self.dy
                self.move_counter += 1

    def squares(self):

        # global current_position, x, y, text
        glTranslatef(0, 0, -7.0)
        # i is the digit, 0 is none
        for i in range(1, len(self.current_position)):
            self.LoadTextures(i)
            cory, corx = self.current_position[i]
            if self.x[i] == 0 and self.y[i] == 0:
                self.x[i] = 1.2 * (corx - 1.0) - 0.5
                self.y[i] = -1.2 * (cory - 1.0) + 0.5

            # glBindTexture(GL_TEXTURE_2D, text[i-1])
            glBegin(GL_QUADS)
            glTexCoord2f(0.0,0.0); glVertex3f(self.x[i] + 0.0, self.y[i] + 0.0, 0.0);
            glTexCoord2f(1.0,0.0); glVertex3f(self.x[i] + 1.0, self.y[i] + 0.0, 0.0);
            glTexCoord2f(1.0,-1.0); glVertex3f(self.x[i] + 1.0, self.y[i] - 1.0, 0.0);
            glTexCoord2f(0.0,-1.0); glVertex3f(self.x[i] + 0.0, self.y[i] - 1.0, 0.0);
            glEnd()

    def DrawGLScene(self):

        global solved

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.squares()
        glutSwapBuffers()
        if self.solved == False:
            self.solve()

    # ウィンドウのサイズが変更されたときに呼び出される関数 (フルスクリーン有効時は使用されないはず)
    def ReSizeGLScene(self, Width, Height):
        if Height == 0:                        # ウィンドウが小さすぎる場合、ゼロによる除算を防ぐ 
            Height = 1

        glViewport(0, 0, Width, Height)        # 現在のビューポートとパースペクティブの変換をリセット
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    # キーボードが押されたときに呼び出される関数
    def keyPressed(self, *args):
        global window
        # ESCを押したときに終了
        # print(args)
        if args[0] == b'0':
            sys.exit()

    # 一般的なOpenGL初期化関数。 すべての初期パラメータを設定する。
    def InitGL(self, Width, Height):              # OpenGLウィンドウが作成された直後にこれを呼び出す
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.0, 0.0, 0.0, 0.0)    # 背景色を黒でクリア
        glClearDepth(1.0)                   # デプスバッファのクリアを有効に
        glDepthFunc(GL_LESS)                # 行うべきDepth Testの種類
        glEnable(GL_DEPTH_TEST)             # Depth Testを可能に
        glShadeModel(GL_SMOOTH)             # スムーズなカラーシェーディングを有効に
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    # 投影マトリックスのリセット
        
        # ウィンドウのアスペクト比を計算
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)

def show_and_solve_puzzle(puzzle, solution):
    sp = ShowPuzzle(puzzle, solution)
    # print("puzzle:", sp.puzzle)
    # print("solution:", sp.solution)
    sp.main()
    return None

def string_to_list(file):
    with open(file) as f:
        s = f.readlines()
        puzzle = ast.literal_eval(s[0].strip())
        solution = ast.literal_eval(s[1])
    return puzzle, solution

if __name__ == '__main__':
    file = 'puzzle.txt'
    puzzle, solution = string_to_list(file)
    show_and_solve_puzzle(puzzle, solution)
