class Timer {
  constructor(duration, startBtn, pauseBtn, callbacks) {
    this.duration = duration;
    this.startBtn = startBtn;
    this.pauseBtn = pauseBtn;

    // can use callbacks/rest args as optional args (hence use if-conditional to check)
    if (callbacks) {
      this.onStart = callbacks.onStart;
      this.onTick = callbacks.onTick;
      this.onComplete = callbacks.onComplete;
    }

    this.startBtn.addEventListener("click", this.start);
    // older, but can also do this.start.call/apply/bind(this) and no arrow func
    this.pauseBtn.addEventListener("click", this.pause);
  }

  // "this" in arrow func is "this" 1 line above "start". But "start" is outside of constructor, so "this" is Window?
  // No, as evident in Babel, underlying implementation is "start" is hoisted up into constructor. so "this" is Timer object
  start = () => {
    if (this.duration.value !== "") {
      if (this.onStart) this.onStart(this.duration.value);
      this.tick();
      this.interval = setInterval(this.tick, 10);
      this.startBtn.disabled = true;
    }
  };

  pause = () => {
    clearInterval(this.interval);
    this.startBtn.disabled = false;
  };

  tick = () => {
    if (this.duration.value > 0) {
      this.duration.value = (this.duration.value - 0.01).toFixed(2);
      if (this.onTick) this.onTick(this.duration.value);
    } else {
      this.pause();
      this.duration.value = "";
      if (this.onComplete) this.onComplete();
    }
  };

  // "get" and "set" keyword enables usage as if an attribute (this.timeRemaining)
  //   get timeRemaining() {
  //     return parseFloat(this.duration.value);
  //   }
  //   set timeRemaining(time) {
  //     this.duration.value = time;
  //   }
}
