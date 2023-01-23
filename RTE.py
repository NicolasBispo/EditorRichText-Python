
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *


#Cria a classe RTE com o parametro do pacote PyQt5.QtGui inicializando a janela principal
class RTE(QMainWindow):

    #Método construtor do objeto
    def __init__(self):
        super(RTE, self).__init__()
        
        #Cria o editor de texto
        self.editor = QTextEdit()
        
        
        
        #Cria a caixa de seleção para o tamanho do texto
        self.caixaSelecaoTamanhoTexto = QSpinBox()

        #Seleciona uma fonte e um tamanho de texto
        fonteInicial = QFont('Times, 12')
        self.editor.setFont(fonteInicial)

        self.path = ""

        #Define o editor de texto como Widget Central
        self.setCentralWidget(self.editor)

        #Dá um nome a janela da aplicação
        self.setWindowTitle("Editor de Texto")

        #Maximiza a janela
        self.showMaximized()

        #Inicializa o carregamento da barra de ferramentas
        self.criar_barra_ferramentas()

        #self.editor.setFontPointSize(24)
    
    def criar_barra_ferramentas(self):

        
        
        #Criando a barra de ferramentas utilizando um componente de QtWidgets
        barra_ferramentas = QToolBar()

        #Criar botão de salvar
        botao_salvar = QAction(QIcon('editorrichtext/src/imgs/btn_salvar.png'), 'Salvar', self)
        botao_salvar.triggered.connect(self.saveFile)
        barra_ferramentas.addAction(botao_salvar)

        #Criando o botão desfazer
        botao_desfazer = QAction(QIcon('editorrichtext/src/imgs/btn_desfazer.png'), 'desfazer',  self)
        botao_desfazer.triggered.connect(self.editor.undo)
        barra_ferramentas.addAction(botao_desfazer)
        
        #Criando o botão refazer
        botao_refazer = QAction(QIcon('editorrichtext/src/imgs/btn_refazer.png'), 'refazer', self)
        botao_refazer.triggered.connect(self.editor.redo)
        barra_ferramentas.addAction(botao_refazer)

        #Criando o botão copiar
        botao_copiar = QAction(QIcon('editorrichtext/src/imgs/btn_copiar.png'), 'copiar', self)
        botao_copiar.triggered.connect(self.editor.copy)
        barra_ferramentas.addAction(botao_copiar)
        
        #Criando o botão cortar
        botao_cortar = botao_copiar = QAction(QIcon('editorrichtext/src/imgs/btn_recortar.png'), 'cortar', self)
        botao_cortar.triggered.connect(self.editor.cut)
        barra_ferramentas.addAction(botao_cortar)

        #Criando o botão colar
        botao_colar = botao_copiar = QAction(QIcon('editorrichtext/src/imgs/btn_colar.png'), 'colar', self)
        botao_colar.triggered.connect(self.editor.paste)
        barra_ferramentas.addAction(botao_colar)
        
        #Cria a caixa de seleção de fontes para serem utilizadas
        self.caixaSelecaoFonte = QComboBox(self)
        self.caixaSelecaoFonte.addItems(["Arial","Arial Black", "Times New Roman", "Comic Sans MS", 'MS Sans Serif'])
        self.caixaSelecaoFonte.activated.connect(self.selecionarFonte)
        barra_ferramentas.addWidget(self.caixaSelecaoFonte)

        
        #Criando a caixa de seleção de cor de texto
        
        
        self.caixaSelecaoCorTexto = QAction(QIcon())

        '''
        Cria a caixa de seleção de tamanho de fonte
        atribui a caixaSelecaoTamanhoTexto a função selecionarTamanhoFonte
        que altera o tamanho da fonte do texto
        '''
        self.caixaSelecaoTamanhoTexto.setValue(24)
        self.caixaSelecaoTamanhoTexto.valueChanged.connect(self.selecionarTamanhoFonte)
        barra_ferramentas.addWidget(self.caixaSelecaoTamanhoTexto)


        #Criar botão alinhar a esquerda
        botao_alinharEsquerda = QAction(QIcon('editorrichtext/src/imgs/btn_alinhar_esquerda.png'), 'Alinhar a esquerda', self)
        botao_alinharEsquerda.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        barra_ferramentas.addAction(botao_alinharEsquerda)

        #Criar botão alinhar ao centro
        botao_alinharCentro = QAction(QIcon('editorrichtext/src/imgs/btn_alinhar_centro.png'), 'Alinhar ao centro', self)
        botao_alinharCentro.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        barra_ferramentas.addAction(botao_alinharCentro)


        #Criar botão alinhar a direita
        botao_alinharDireita = QAction(QIcon('editorrichtext/src/imgs/btn_alinhar_direita.png'), 'Alinhar a direita', self)
        botao_alinharDireita.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        barra_ferramentas.addAction(botao_alinharDireita)

        #Cria o botão negrito
        botao_negrito = QAction(QIcon('editorrichtext/src/imgs/btn_negrito.png'), 'Negrito', self)
        botao_negrito.triggered.connect(self.colocarNegrito)
        barra_ferramentas.addAction(botao_negrito)

        #Cria o botão sublinhar
        botao_sublinhar = QAction(QIcon('editorrichtext/src/imgs/btn_sublinhar.png'), 'Sublinhar', self)
        botao_sublinhar.triggered.connect(self.colocarSublinhado)
        barra_ferramentas.addAction(botao_sublinhar)

        #Criar o botão itálico
        botao_italico = QAction(QIcon('editorrichtext/src/imgs/btn_italico.png'), 'Itálico', self)
        botao_italico.triggered.connect(self.colocarItalico)
        barra_ferramentas.addAction(botao_italico)

        self.addToolBar(barra_ferramentas)
    

    #Função para selecionar tamanho do texto
    def selecionarTamanhoFonte(self):
        tamanho_fonte = self.caixaSelecaoTamanhoTexto.value()
        self.editor.setFontPointSize(tamanho_fonte)

    #Função para selecionar fonte
    def selecionarFonte(self):
        fonte_selecionada = self.caixaSelecaoFonte.currentText()
        self.editor.setCurrentFont(QFont(fonte_selecionada))

    def colocarNegrito(self):
        negrito = self.editor.fontWeight() == QFont.Bold
        self.editor.setFontWeight(QFont.Normal if negrito else QFont.Bold)
    
    def colocarSublinhado(self):
        estilo = self.editor.fontUnderline()
        self.editor.setFontUnderline(not(estilo))   
    
    def colocarItalico(self):
        estilo = self.editor.fontItalic()
        self.editor.setFontItalic(not(estilo))

    def saveFile(self):
        print(self.path)
        if self.path == '':
            self.file_saveas()
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)
        
    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text documents (*.text);Text documents (*.txt);All files (*.*)")
        if self.path == '':
            return
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
                print(e)


app = QApplication(sys.argv)
window = RTE()
window.show()
sys.exit(app.exec_())