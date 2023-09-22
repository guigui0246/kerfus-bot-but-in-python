module.exports = (req,res,next) => {
    let useragent = "";
    for(let a=0;a<req.rawHeaders.length;a+=2){
      if(req.rawHeaders[a]=='User-Agent')useragent=req.rawHeaders[a+1];
    }
    if(!/chrom/i.test(useragent)){next();return;}
    res.send('<!DOCTYPE html><html><head><title>Browser not supported</title></head><body><h1>Browser not supported</h1><br>Sorry, but im not currently supporting chromium-based browsers<br>Please switch to something like <a href="https://www.mozilla.org/en-US/firefox/new/">Firefox</a></body></html>');
  }