/* Shared source: generated for each edition with localized messages. */
(() => {
  'use strict';
  const messages = __MESSAGES__;
  const $ = id => document.getElementById(id);
  const value = id => Number($(id).value);
  const path = (points, color, dash = '') => `<polyline points="${points.map(p => p.join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}"/>`;
  const axes = (x = 65, y = 270) => `<path d="M25 ${y}H580M${x} 35V290" stroke="#5f7470" fill="none"/>`;
  const label = text => `<text x="30" y="22">${text}</text>`;
  const green = '#086a67', orange = '#bd6029', gray = '#5f7470';

  function derivative() {
    const h = value('h'), xy = (x, y) => [65 + x * 200, 270 - y * 55];
    const points = Array.from({length: 75}, (_, i) => xy(i * .03, (i * .03) ** 2));
    $('derivative-svg').innerHTML = axes() + path(points, green)
      + path([xy(0, -1), xy(2.3, 3.6)], gray, '6 5')
      + path([xy(.5, 1 - (2 + h) * .5), xy(2, 1 + (2 + h))], orange)
      + [xy(1, 1), xy(1 + h, (1 + h) ** 2)].map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="${orange}"/>`).join('')
      + `<text x="280" y="220">${messages.fixed}</text>`;
    $('h-out').textContent = `h=${h.toFixed(2)}; ${messages.secant}=${(2 + h).toFixed(2)}; ${messages.tangent}=2`;
  }

  function linear() {
    const a = value('a');
    $('linear-svg').innerHTML = axes(300, 250)
      + `<rect x="300" y="160" width="90" height="90" fill="none" stroke="${gray}" stroke-dasharray="6 4"/><rect x="${Math.min(300, 300 + a * 90)}" y="160" width="${Math.abs(a * 90)}" height="90" fill="#147d7866" stroke="${green}"/>`
      + label(messages.unit);
    $('a-out').textContent = `a=${a.toFixed(1)}; det(A)=${a.toFixed(1)}; ${messages.area}=${Math.abs(a).toFixed(1)}`;
  }

  function probability() {
    const p = value('p');
    let bars = '', sum = 0, coefficient = 1;
    for (let k = 0; k <= 10; k++) {
      if (k) coefficient *= (11 - k) / k;
      const mass = coefficient * p ** k * (1 - p) ** (10 - k);
      sum += mass;
      bars += `<rect x="${40 + k * 48}" y="${270 - mass * 230}" width="32" height="${mass * 230}" fill="${green}"><title>k=${k}, P=${mass.toFixed(5)}</title></rect><text x="${45 + k * 48}" y="295">${k}</text>`;
    }
    $('prob-svg').innerHTML = '<path d="M25 270H580" stroke="#5f7470" fill="none"/>' + bars + label(messages.probability);
    $('p-out').textContent = `p=${p.toFixed(2)}; ${messages.expectation}=${(10 * p).toFixed(2)}; ${messages.variance}=${(10 * p * (1 - p)).toFixed(2)}; ${messages.sum}=${sum.toFixed(6)}`;
  }

  function euler() {
    const step = value('step'), points = [[0, 1]];
    let y = 1;
    for (let j = 1; j * step <= 10 + 1e-9; j++) {
      y *= 1 - 2 * step;
      points.push([j * step, y]);
    }
    const scale = Math.max(1, ...points.map(p => Math.abs(p[1])));
    const position = (t, v) => [45 + t * 52, 155 - v / scale * 120];
    const exact = Array.from({length: 201}, (_, i) => position(i / 20, Math.exp(-i / 10)));
    $('euler-svg').innerHTML = axes(45, 155) + path(exact, green)
      + path(points.map(([t, v]) => position(t, v)), orange)
      + label(`${messages.range} ±${scale.toFixed(2)}; ${messages.time}`);
    $('step-out').textContent = `h=${step.toFixed(1)}; ${messages.factor}=${(1 - 2 * step).toFixed(2)}; ${messages.last} t=${points.at(-1)[0].toFixed(1)}, y≈${y.toFixed(5)}`;
  }

  function sampling() {
    const n = value('n'), groups = 2000, counts = new Array(n + 1).fill(0);
    let sum = 0, squares = 0;
    for (let g = 0; g < groups; g++) {
      let heads = 0;
      for (let i = 0; i < n; i++) if (Math.random() < .5) heads++;
      counts[heads]++;
      sum += heads / n;
      squares += (heads / n) ** 2;
    }
    // Each bar has bin width 1/n. Its area is count/groups, just like a density.
    // A single y scale preserves the comparison with the theoretical normal PDF.
    const width = 1 / n, sd = Math.sqrt(.25 / n), peak = 1 / (sd * Math.sqrt(2 * Math.PI));
    const densities = counts.map(count => count / (groups * width));
    const top = Math.max(peak, ...densities) * 1.08;
    const left = -width / 2, extent = 1 + width;
    const px = x => 45 + (x - left) / extent * 520, py = y => 270 - y / top * 225;
    const bars = densities.map((density, k) => `<rect x="${px((k - .5) / n)}" y="${py(density)}" width="${520 * width / extent}" height="${270 - py(density)}" fill="${green}" stroke="#f4f7f4" stroke-width=".5"><title>${k}/${n}: ${counts[k]} ${messages.groups}; ${messages.density}=${density.toFixed(4)}</title></rect>`).join('');
    const curve = Array.from({length: 241}, (_, i) => {
      const x = left + extent * i / 240;
      return [px(x), py(peak * Math.exp(-((x - .5) ** 2) / (2 * sd * sd)))];
    });
    const ticks = [0, .5, 1].map(x => `<text x="${px(x)}" y="295" text-anchor="middle">${x}</text>`).join('');
    $('clt-svg').innerHTML = axes(45, 270) + bars + path(curve, gray, '6 5') + ticks + label(messages.clt)
      + `<text x="5" y="48">${top.toFixed(2)}</text>`;
    const mean = sum / groups, sampleSD = Math.sqrt(Math.max(0, squares / groups - mean * mean));
    $('n-out').textContent = `n=${n}; ${messages.theorySD}=√(0.25/n)=${sd.toFixed(4)}; ${messages.sampleSD}=${sampleSD.toFixed(4)}; ${messages.mean}≈${mean.toFixed(3)}`;
  }

  function newton() {
    const f = x => x ** 3 - 2 * x + 2, fp = x => 3 * x * x - 2;
    const px = x => 45 + (x + 2.5) / 5 * 520, py = y => 270 - (y + 10) / 24 * 225;
    let x = value('x0'), lines = '', dots = '', status = messages.limit;
    const list = [x];
    for (let i = 0; i < 8; i++) {
      if (Math.abs(f(x)) < 1e-10) { status = messages.converged; break; }
      const slope = fp(x);
      if (Math.abs(slope) < 1e-6) { status = messages.flat; break; }
      const next = x - f(x) / slope;
      lines += path([[px(x), py(f(x))], [px(next), py(0)]], orange, '4 4');
      dots += `<circle cx="${px(x)}" cy="${py(f(x))}" r="4" fill="${orange}"/>`;
      const repeated = list.some(previous => Math.abs(previous - next) < 1e-10);
      list.push(next);
      x = next;
      if (Math.abs(f(x)) < 1e-10) { status = messages.converged; break; }
      if (repeated) { status = messages.cycle; break; }
      if (!Number.isFinite(x) || Math.abs(x) > 2.5) { status = messages.escaped; break; }
    }
    const curve = Array.from({length: 201}, (_, i) => {
      const t = -2.5 + i / 40;
      return [px(t), py(f(t))];
    });
    // Clip geometry at the viewport, never the mathematical function values.
    $('newton-svg').innerHTML = '<defs><clipPath id="newton-clip"><rect x="45" y="40" width="520" height="230"/></clipPath></defs>'
      + axes(px(0), py(0)) + `<g clip-path="url(#newton-clip)">${path(curve, green)}${lines}${dots}</g>`
      + label(messages.newton) + '<text x="45" y="295">x=−2.5</text><text x="515" y="295">x=2.5</text>';
    $('x0-out').textContent = `${messages.iteration}: ${list.slice(0, 5).map(v => v.toFixed(3)).join(' → ')}${list.length > 5 ? ' → …' : ''}; ${messages.residual} f(x${list.length - 1})=${f(x).toFixed(6)}; ${status}`;
  }

  function eigen() {
    const a = value('ea'), b = value('eb'), d = value('ed');
    const radius = Math.hypot(a - d, 2 * b), l1 = (a + d + radius) / 2, l2 = (a + d - radius) / 2;
    const angle = .5 * Math.atan2(2 * b, a - d), u = [Math.cos(angle), Math.sin(angle)], v = [-u[1], u[0]];
    const position = (x, y) => [300 + x * 40, 165 - y * 40];
    const circle = [], ellipse = [];
    for (let i = 0; i <= 120; i++) {
      const t = i / 120 * 2 * Math.PI, x = Math.cos(t), y = Math.sin(t);
      circle.push(position(x, y)); ellipse.push(position(a * x + b * y, b * x + d * y));
    }
    $('eigen-svg').innerHTML = path(circle, gray, '6 5') + path(ellipse, green)
      + path([position(-l1 * u[0], -l1 * u[1]), position(l1 * u[0], l1 * u[1])], orange)
      + path([position(-l2 * v[0], -l2 * v[1]), position(l2 * v[0], l2 * v[1])], orange, '4 4')
      + label(messages.eigen);
    $('e-out').textContent = `A=[[${a.toFixed(1)},${b.toFixed(1)}],[${b.toFixed(1)},${d.toFixed(1)}]]; λ₁=${l1.toFixed(3)}, λ₂=${l2.toFixed(3)}; ${messages.semiaxes}=${Math.abs(l1).toFixed(3)}, ${Math.abs(l2).toFixed(3)}; det=${(a * d - b * b).toFixed(3)}=λ₁λ₂; ${messages.areaFactor}=|det|=${Math.abs(a * d - b * b).toFixed(3)}`;
  }

  // A slider updates only its own experiment; other experiments retain their data.
  const experiments = [
    [['h'], derivative], [['a'], linear], [['p'], probability], [['step'], euler],
    [['n'], sampling], [['x0'], newton], [['ea', 'eb', 'ed'], eigen],
  ];
  for (const [ids, render] of experiments) {
    if (!ids.every(id => $(id))) continue;
    for (const id of ids) $(id).addEventListener('input', render);
    render();
  }
  if ($('resample')) $('resample').addEventListener('click', sampling);
})();
