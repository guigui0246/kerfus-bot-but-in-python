class Seed {
  seeder;
  constructor(seed) {
    this.seeder = this.xmur3(seed);
  }

  random(min = 0, max = 1) {
    if (min > max)  
      throw new Error("The minimum value must be below the maximum value");
    if (min == max) 
      return min;
    return this.denormalize(this.sfc32(), min, max);
  }

  randomInt(min = 0, max = 1) {
    return Math.round(this.random(min, max));
  }

  denormalize(value, min, max) {
    return value * (max - min) + min;
  }

  xmur3(str) {
    let h = 1779033703 ^ str.length;
    for(let i of str){
      h = Math.imul(h ^ i.charCodeAt(), 3432918353);
      h = h << 13 | h >>> 19;
    }
    
    return () => {
      h = Math.imul(h ^ h >>> 16, 2246822507);
      h = Math.imul(h ^ h >>> 13, 3266489909);
      return (h ^= h >>> 16) >>> 0;
    }
  }

  sfc32() {
    let a = this.seeder(),b = this.seeder(),c = this.seeder(),d = this.seeder();
    a >>>= 0;
    b >>>= 0;
    c >>>= 0;
    d >>>= 0;
    let t = (a + b) | 0;
    a = b ^ (b >>> 9);
    b = (c + (c << 3)) | 0;
    c = (c << 21) | (c >>> 11);
    d = (d + 1) | 0;
    t = (t + d) | 0;
    c = (c + t) | 0;
    return (t >>> 0) / 4294967296;
  }
}

module.exports = Seed;