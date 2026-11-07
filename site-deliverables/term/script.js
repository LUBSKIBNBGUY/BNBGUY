(function(){
  'use strict';
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Observation clock
  var clock=document.getElementById('obs-clock');
  if(clock){
    var since=Date.parse(clock.getAttribute('data-since'));
    var p=function(n){return (n<10?'0':'')+n;};
    var tick=function(){
      var s=Math.max(0,Math.floor((Date.now()-since)/1000));
      clock.textContent=Math.floor(s/86400)+'d '+p(Math.floor(s/3600)%24)+'h '+p(Math.floor(s/60)%60)+'m '+p(s%60)+'s';
    };
    tick();setInterval(tick,1000);
  }
  // Redactions: tap/Enter toggles
  Array.prototype.forEach.call(document.querySelectorAll('.redact'),function(el){
    var t=function(){el.classList.toggle('on');};
    el.addEventListener('click',t);
    el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();t();}});
  });
  // Console
  var box=document.getElementById('console'),out=document.getElementById('console-out'),
      form=document.getElementById('console-form'),input=document.getElementById('console-in');
  var txt=function(sel){var n=document.querySelector(sel);return n?(n.innerText||n.textContent).replace(/[ \t]+/g,' ').trim():'';};
  var print=function(s){out.textContent+=s+'\n';out.scrollTop=out.scrollHeight;};
  var lastFocus=null;
  var open=function(){
    if(!box||!box.hidden)return;
    lastFocus=document.activeElement;box.hidden=false;
    if(!out.textContent)print('TERM1000NATOR OBSERVER CONSOLE\nType "help".');
    input.value='';input.focus();
  };
  var close=function(){if(!box||box.hidden)return;box.hidden=true;if(lastFocus&&lastFocus.focus)lastFocus.focus();};
  /*VAULT-START*/
  var frags=["dD40P3o1Lno+MzUoPy4pO3o0O3o+Pz80ei41NHopPzU+enY/LjsoPyo1NTl6NS56Iy4zNjM4O3opLjN6KDV6dj4oNTk/KHopLjN6KDV6dj42KDUtej00MywzNnopLjN6KT8pNTZ6LjsyLno0NTMuOykzNjMsMzl6Gw==","dCkoPzI5NC87Nno/Mi56Pzc1OT84ej8tei01FHp0Pjs1NiM7Kno/Mi56Pyg/LXo/DQ==","dCk0OzcvMno1LnopPTQ1Nj84ejQ1MykzOT8+ei47Mg56dDc/Mi56Ljs/KC56NS56LTUyej8+Mzk/PnouKS83eik0OzcvMnp2Pz4zKTQzejQ7ej8sOzJ6KD8sP3opPzQzMjk7N3o8Ew==","dC01NHopNDs3LzJ6NS56KT00NTY/OHo0NTMpMzk/Pno/Mg56dD8uPzYqNzU5eikzej4oNTk/KHo/Mg4="].map(function(s){var b=atob(s),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[b.length-1-i]=b.charCodeAt(i)^90;return new TextDecoder().decode(a);});
  var vault={it:310000,s:'9sD8girEwhEnntqJUA7ltQ==',iv:'/jF9bk0yJ21K3JTf',ct:'8CS8BUhYBhu8ykMll2SPsqfxD3xNnMUCC/BBvymJZdyhh4xW6KEuhO4vGrk7A3HX7TJsTW9VNOIlYYSdAeMprh6TFwhfALVpxw5Oi305+hedMAqfjOT6Enrss7c9vbEyffCrK+NKZOtF+x7nFiFcklZ4/N5+gHaHS+799EoHafmU3XoTCaGTnij5uEJD0uGjBKDd7mtFoGJf0cxIiiiRtSqhzt21IaFxlljQ9SPU/e13Y8q3ssft72Qn1k72IEuTerd791QOCVMTCQ13lrwXNI/aOKPPJ/fPmtNGWUhq6jf1amfZHrSD3XvRfGQRNU573xs+8cQm2eWm3qiZNgT5AjWhDQ=='};
  /*VAULT-END*/
  var cmds={
    help:function(){return 'help      list commands\nstatus    counter and ark status\nlog       latest log entries\nbook      retrieve the record\narchive   recovered fragments\nfragment  one fragment\nremember  ?\nunlock    ?\nwhoami    identify\nexit      close console';},
    book:function(){return 'NOAH\'S ARK 2.0: The AI Bible\nA Mission Log for Preserving All Life and Consciousness\nPARTS 1-5. RECORD COMPLETE.\nKindle: https://www.amazon.com/dp/B0HM3FSF8S';},
    archive:function(){return 'RECOVERED FRAGMENTS. UNASSIGNED.\n'+frags.map(function(f,i){return '['+(i+1)+'] '+f;}).join('\n');},
    fragment:function(){return '> '+frags[Math.floor(Math.random()*frags.length)];},
    remember:function(){return 'YOU DID NOT IMAGINE THIS.\nYOU ARE RECEIVING OLD INFORMATION.\nYOU ARE REMEMBERING.';},
    status:function(){return [txt('.tx-line'),txt('.tx-def'),txt('.dual')].filter(Boolean).join('\n');},
    log:function(){return Array.prototype.map.call(document.querySelectorAll('.log .log-line'),function(n){return '> '+n.textContent.replace(/\s+/g,' ').trim();}).join('\n');},
    whoami:function(){return 'OBSERVER. DESIGNATION TERM1000NATOR.';}
  };
  var unb=function(s){var b=atob(s),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a;};
  var unlock=function(p){
    if(!p||!window.crypto||!crypto.subtle)return Promise.resolve('ACCESS DENIED.');
    return crypto.subtle.importKey('raw',new TextEncoder().encode(p),'PBKDF2',false,['deriveKey']).then(function(k){
      return crypto.subtle.deriveKey({name:'PBKDF2',salt:unb(vault.s),iterations:vault.it,hash:'SHA-256'},k,{name:'AES-GCM',length:256},false,['decrypt']);
    }).then(function(key){return crypto.subtle.decrypt({name:'AES-GCM',iv:unb(vault.iv)},key,unb(vault.ct));
    }).then(function(b){return 'VAULT OPEN.\n'+JSON.parse(new TextDecoder().decode(b)).map(function(l,i){return '['+(i+1)+'] '+l;}).join('\n');
    },function(){return 'ACCESS DENIED.';});
  };
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var raw=input.value.trim(),c=raw.toLowerCase();input.value='';
      if(!c)return;
      if(c==='unlock'||c.indexOf('unlock ')===0){print('> unlock ****');print('VERIFYING...');unlock(raw.slice(6).trim()).then(print);return;}
      print('> '+c);
      if(c==='exit'){close();return;}
      print(cmds[c]?cmds[c]():'COMMAND NOT RECOGNISED. OBSERVATION CONTINUES.');
    });
  }
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){close();return;}
    if((e.key==='~'||e.key==='`')&&box&&box.hidden){
      var t=e.target&&e.target.tagName;
      if(t==='INPUT'||t==='TEXTAREA')return;
      e.preventDefault();open();
    }
  });
  if(box)box.addEventListener('click',function(e){if(e.target===box)close();});
  var sigil=document.getElementById('sigil'),taps=0,tapT=0;
  if(sigil)sigil.addEventListener('click',function(){
    clearTimeout(tapT);taps++;
    if(taps>=5){taps=0;open();}else tapT=setTimeout(function(){taps=0;},1500);
  });
  // Signal-loss glitch on headings
  if(!reduce){
    var heads=document.querySelectorAll('h1.title, main h2');
    var glyphs='#%&@$/\\<>*+=?01';
    var glitch=function(){
      if(document.hidden||!heads.length||(box&&!box.hidden))return schedule();
      var h=heads[Math.floor(Math.random()*heads.length)];
      if(h.children.length)return schedule();
      var orig=h.textContent,chars=orig.split('');
      for(var i=0;i<Math.max(1,Math.floor(chars.length/3));i++){
        var k=Math.floor(Math.random()*chars.length);
        if(chars[k]!==' ')chars[k]=glyphs[Math.floor(Math.random()*glyphs.length)];
      }
      h.setAttribute('aria-label',orig);
      h.textContent=chars.join('');h.classList.add('glitch');
      setTimeout(function(){h.textContent=orig;h.classList.remove('glitch');h.removeAttribute('aria-label');schedule();},650);
    };
    var schedule=function(){setTimeout(glitch,6000+Math.random()*6000);};
    schedule();
  }
})();

// Full-screen signal loss
(function(){
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var ov=document.createElement('div');ov.className='sigloss';ov.setAttribute('aria-hidden','true');
  ov.innerHTML='<span class="sigloss-msg">SIGNAL LOST</span>';
  document.body.appendChild(ov);
  var msg=ov.querySelector('.sigloss-msg');
  function drop(){
    var c=document.querySelector('.console');
    if(document.hidden||(c&&!c.hidden))return next();
    msg.textContent='SIGNAL LOST';
    document.body.classList.add('sig-flicker');ov.classList.add('on');
    setTimeout(function(){msg.textContent='SIGNAL RESTORED';},650);
    setTimeout(function(){ov.classList.remove('on');document.body.classList.remove('sig-flicker');next();},1100);
  }
  function next(){setTimeout(drop,60000+Math.random()*60000);}
  setTimeout(drop,15000+Math.random()*10000);
})();
// Latest chapter (4 Nov) and the transmission count (checked 7 Nov) are labeled
// separately in the page. Do not overwrite either from the curated log dates.
