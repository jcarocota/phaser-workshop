// Configuración básica de Phaser
const config = {
  type: Phaser.AUTO,
  width: 400,
  height: 600,
  physics: {
      default: 'arcade',
      arcade: {
          gravity: { y: 600 },
          debug: false
      }
  },
  scene: {
      preload: preload,
      create: create,
      update: update
  }
};

const game = new Phaser.Game(config);
let bird;
let pipes;
let pipeTimer;
let score;
let scoreText;
let gameOver = false;

//PASO #3
let initialGapSize = 500;      // Valor inicial del gap
let finalGapSize = 150;        // Valor final del gap
let gapChangeDuration = 60;    // Duración en segundos para el cambio (puedes ajustarlo)
let gapSize = initialGapSize;  // Valor actual, que se actualizará
let startTime;  // Para almacenar el tiempo en que inicia la escena

//PASO #3
// Variables globales para la velocidad dinámica de las tuberías
let initialPipeSpeed = -200;      // Velocidad inicial (px/s)
let finalPipeSpeed = -500;        // Velocidad final (px/s)
let pipeSpeedChangeDuration = 60; // Duración en segundos para alcanzar la velocidad final
let currentPipeSpeed = initialPipeSpeed;

//PASO #4
// Variables globales para el cronómetro
let timerText;


function preload() {
  // Usamos Graphics para crear texturas simples sin depender de archivos externos.
  // Creamos una textura para el pájaro (un rectángulo amarillo).
  this.graphics = this.add.graphics();
  this.graphics.fillStyle(0xffff00, 1);
  this.graphics.fillRect(0, 0, 34, 24);
  this.graphics.generateTexture('bird', 34, 24);
  this.graphics.clear();
  
  // Creamos una textura para las tuberías (rectángulo verde)
  this.graphics.fillStyle(0x00ff00, 1);
  this.graphics.fillRect(0, 0, 50, 300);
  this.graphics.generateTexture('pipe', 50, 300);
  this.graphics.destroy(); // Destruimos el objeto graphics ya que no es necesario

  //Cargar textura del cielo #PASO2
  this.load.image('background', 'assets/sky_pixel_clouds.png');
  this.load.image('pipeTexture', 'assets/pipe_segment.png');
  this.load.spritesheet('birdSpriteTexture', 'assets/bird_anim.png', { frameWidth: 68, frameHeight: 48 });
  this.load.image('kaboomSign', 'assets/kaboom_sign.png');
  this.load.spritesheet('boom', 'assets/boom_spritesheet.png', { frameWidth: 50, frameHeight: 50 });

  //PASO #5
  // Otros assets...
  this.load.audio('jump', 'assets/sounds/flap_jump.wav');
  this.load.audio('kaboom', 'assets/sounds/kaboom_explosion.wav');
  this.load.audio('start', 'assets/sounds/game_start.wav');
}

function create() {
  // Guardar el tiempo de inicio (en milisegundos)
  startTime = this.time.now;

  // Reiniciar variables del juego
  gameOver = false;
  score = -1;

  //PASO #5
  //Creación de sonidos
  jumpSound = this.sound.add('jump');
  kaboomSound = this.sound.add('kaboom');
  startSound = this.sound.add('start');

  // Reproducir sonido de inicio cuando arranca el juego
  startSound.play();


  //Agregar cielo como fondo PASO #2
  this.add.image(0, 0, 'background').setOrigin(0, 0).setDisplaySize(400, 600);

  // Crear la animación de aleteo para el pájaro PASO #2
  this.anims.create({
    key: 'flap',
    frames: this.anims.generateFrameNumbers('birdSpriteTexture', { start: 0, end: 2 }),
    frameRate: 10,  // Puedes ajustar la velocidad de la animación
    repeat: -1      // Se repetirá indefinidamente
  });
  
  // Agregar el pájaro y habilitar su física
  //bird = this.physics.add.sprite(100, 300, 'bird');
  //PASO #2
  bird = this.physics.add.sprite(100, 300, 'birdSpriteTexture').play('flap');

  bird.setCollideWorldBounds(true);
  
  // Crear un grupo para las tuberías
  pipes = this.physics.add.group();
  
  // Configurar el input: al hacer clic o presionar la barra espaciadora, el pájaro salta
  this.input.on('pointerdown', flap, this);
  this.input.keyboard.on('keydown-SPACE', flap, this);
  
  // Detectar colisión entre el pájaro y las tuberías
  this.physics.add.overlap(bird, pipes, hitPipe, null, this);
  
  // Mostrar el puntaje en pantalla
  scoreText = this.add.text(10, 10, 'Puntaje: 0', { fontFamily: 'PressStar2P', fontSize: '14px', fill: '#fff', stroke: '#000',  strokeThickness: 3 });
  scoreText.setDepth(1000);

  // Cronómetro (debajo del score, por ejemplo, en y = 40)
  timerText = this.add.text(10, 40, 'Tiempo: 0s', {
    fontFamily: 'PressStar2P',
    fontSize: '14px',
    fill: '#32CD32',
    stroke: '#000',
    strokeThickness: 3
  });
  timerText.setDepth(1000);

  //PASO #2
  // Definir la animación de explosión
  this.anims.create({
    key: 'boom_anim',
    frames: this.anims.generateFrameNumbers('boom', { start: 0, end: 3 }),
    frameRate: 10,
    hideOnComplete: true // Oculta (o destruye) el sprite cuando la animación termina
  });
  
  // Generar tuberías cada 1.5 segundos
  pipeTimer = this.time.addEvent({
      delay: 1500,
      callback: addRowOfPipes,
      callbackScope: this,
      loop: true
  });
}

function update() {
  if (gameOver) {
      return;
  }

  //PASO #3
   // Actualizar el gapSize de forma lineal
   let elapsed = (this.time.now - startTime) / 1000; // segundos transcurridos
  
   if (elapsed < gapChangeDuration) {
    // Lerp lineal: gapSize disminuye de initialGapSize a finalGapSize en gapChangeDuration segundos
    gapSize = initialGapSize - ((initialGapSize - finalGapSize) * (elapsed / gapChangeDuration));
  } else {
    gapSize = finalGapSize;
  }

  //PASO #3
  if (elapsed < pipeSpeedChangeDuration) {
    // Interpolación lineal para la velocidad
    currentPipeSpeed = initialPipeSpeed + ((finalPipeSpeed - initialPipeSpeed) * (elapsed / pipeSpeedChangeDuration));
  } else {
    currentPipeSpeed = finalPipeSpeed;
  }

  //PASO #4
  // Actualizar el cronómetro solo si el juego sigue en curso
  let elapsedFloor = Math.floor(elapsed*10)/10;
  timerText.setText('Tiempo: ' + elapsedFloor.toFixed(1) + 's');


  // Si el pájaro se sale verticalmente, se considera colisión
  //if (bird.y < 0 || bird.y > config.height) {
  //    hitPipe.call(this);
  //}
  
  // Eliminar las tuberías que han salido completamente de la pantalla
  pipes.getChildren().forEach(function(pipe) {
      if (pipe.x < -pipe.width) {
          pipes.remove(pipe, true, true);
      }
  });
}

function flap() {
  if (gameOver) return;
  // Aplica una velocidad negativa para simular el salto
  jumpSound.play();
  bird.setVelocityY(-300);
}

function addRowOfPipes() {
  // Define la posición del hueco (gap) de forma aleatoria
  let gap = Phaser.Math.Between(100, 400);
  //let gapSize = 200; // Tamaño del espacio libre entre tuberías
  
  // Tubería superior: se crea partiendo desde el borde inferior de la imagen
  //let topPipe = pipes.create(config.width, gap - gapSize / 2, 'pipe');
  //PASO #2
  let topPipe = pipes.create(config.width, gap - gapSize / 2, 'pipeTexture');
  topPipe.setOrigin(0, 1); // Hace que la imagen se extienda hacia abajo
  topPipe.body.allowGravity = false;
  //topPipe.setVelocityX(-200);
  //PASO #3
  topPipe.setVelocityX(currentPipeSpeed);
  
  // Tubería inferior: se crea a partir del borde superior
  //let bottomPipe = pipes.create(config.width, gap + gapSize / 2, 'pipe');
  //PASO #2
  let bottomPipe = pipes.create(config.width, gap + gapSize / 2, 'pipeTexture');
  bottomPipe.setOrigin(0, 0);
  bottomPipe.body.allowGravity = false;
  //bottomPipe.setVelocityX(-200);
  //PASO #3
  bottomPipe.setVelocityX(currentPipeSpeed);
  
  // Actualizar el puntaje
  score += 1;
  scoreText.setText('Puntaje: ' + score);
}

function hitPipe(bird, pipe) {
  // Se invoca cuando el pájaro colisiona con una tubería o sale de los límites
  if (!gameOver) {
      gameOver = true;
      // Detener la generación de tuberías
      pipeTimer.remove(false);

      //PASO #2
      // Guardar la posición del pájaro antes de destruirlo
      let boomX = pipe.x;
      let boomY = bird.y;

      //PASO #2
      // Destruir el pájaro
      bird.destroy();

      //// Crear el sprite de explosión en la posición del pájaro
      let boomSprite = this.physics.add.sprite(boomX, boomY, 'boom').setOrigin(0.5);
      boomSprite.play('boom_anim');
      // Evitar que la gravedad afecte la explosión
      boomSprite.body.allowGravity = false;
      // Asignar la misma velocidad horizontal que las tuberías (por ejemplo, -200)
      boomSprite.setVelocityX(-200);

      kaboomSound.play();

      //PASO #2
      // Mostrar el letrero "¡kaboom!" en el centro del juego
      let kaboomSign = this.add.image(config.width / 2, config.height / 2, 'kaboomSign').setOrigin(0.5);

      // Opcional: puedes agregar un tween para darle un efecto de aparición
      this.tweens.add({
        targets: kaboomSign,
        alpha: { from: 0, to: 1 },
        duration: 500,
        ease: 'Power2'
     });
      
      // Mostrar mensaje de Game Over con el puntaje final
      scoreText.setText('Game Over! Puntaje: ' + score);

      //PASO #4
      timerText.setStyle({ fill: '#ff0000' });
      
      // Reiniciar el juego después de 2 segundos
      this.time.addEvent({
          delay: 2000,
          callback: () => {
              this.scene.restart();
          },
          callbackScope: this
      });
  }
}
