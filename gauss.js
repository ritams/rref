function latex(a) {
  n = a.n;
  d = a.d;
  if (d != 1) {
    if (a.s > 0) {
      return `\\frac{${n}}{${d}}`;
    } else {
      return `-\\frac{${n}}{${d}}`;
    }
  } else {
    if (a.s > 0) {
      return `${n}`;
    } else {
      return `-${n}`;
    }
  }
}

function multiply(i, a) {
  return `R_{${i + 1}} \\rightarrow R_{${i + 1}} \\times (${latex(a)}) \\\\`;
}

function add(i, j, a) {
  return `R_{${j + 1}} \\rightarrow R_{${j + 1}} + R_{${
    i + 1
  }} \\times (${latex(a)}) \\\\`;
}

function swap(i, j) {
  return `R_{${i + 1}} \\leftrightarrow R_{${j + 1}} \\\\`;
}

function augmented(a) {
  let text = "";
  let m = a.length;
  let n = a[0].length;
  let aug = "";
  for (let i = 0; i < n - 1; i++) {
    aug = aug + "c";
  }
  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      text = text + latex(a[i][j]);
      text = text + "&";
    }
    text = text.substring(0, text.length - 1) + "\\\\";
  }
  tex = "\\left[\\begin{array}" + "{" + aug + "|c}";
  tex = tex + text;
  tex = tex + "\\end{array}\\right]";
  return tex;
}

function rref(a) {
  let m = a.length;
  let n = a[0].length;
  let tex = augmented(a);

  for (let i = 0; i < m; i++) {
    let text = [];
    // find pivotal element
    if (a[i][i] != 0) {
      if (a[i][i] != 1) {
        text.push(multiply(i, math.fraction(1, 1).div(a[i][i])));
        let temp = a[i][i];
        for (let j = 0; j < n; j++) {
          a[i][j] = a[i][j].div(temp);
        }
      }
      for (let j = 0; j < m; j++) {
        if (i != j) {
          temp = a[j][i];
          if (temp != 0) {
            text.push(add(i, j, a[j][i].neg()));
            for (let k = 0; k < n; k++) {
              a[j][k] = a[j][k].sub(a[i][k].mul(temp));
            }
          }
        }
      }
    } else {
      let flag = true;
      for (let j = i + 1; j < m; j++) {
        if (a[j][i] != 0) {
          // # swap
          text.push(swap(i, j));
          temp = a[i];
          a[i] = a[j];
          a[j] = temp;
          flag = false;
          break;
        }
      }
      if (flag) {
        break;
      } else {
        if (a[i][i] != 1) {
          text.push(multiply(i, math.fraction(1, 1).div(a[i][i])));
          let temp = a[i][i];
          for (let j = 0; j < n; j++) {
            a[i][j] = a[i][j].div(temp);
          }
        }
        for (let j = 0; j < m; j++) {
          if (i != j) {
            temp = a[j][i];
            if (temp != 0) {
              text.push(add(i, j, a[j][i].neg()));
              for (let k = 0; k < n; k++) {
                a[j][k] = a[j][k].sub(a[i][k].mul(temp));
              }
            }
          }
        }
      }
    }
    let count = text.length;

    up_stack = "\\substack { ";
    down_stack = "\\substack { ";

    for (let j = 0; j < count; j++) {
      if (j < Math.floor(count / 2)) {
        up_stack += text[j];
      } else {
        down_stack += text[j];
      }
    }
    up_stack += " }";
    down_stack += " }";

    let op = `\\xrightarrow[ ${down_stack} ]{ ${up_stack} }`;
    tex = tex + op + augmented(a);
  }
  return tex;
}
