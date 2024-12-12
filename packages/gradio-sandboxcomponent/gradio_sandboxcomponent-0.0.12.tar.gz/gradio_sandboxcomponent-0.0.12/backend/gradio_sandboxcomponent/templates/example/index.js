const {
  SvelteComponent: _,
  append_hydration: m,
  attr: n,
  children: d,
  claim_element: f,
  detach: c,
  element: h,
  init: g,
  insert_hydration: v,
  noop: u,
  safe_not_equal: y,
  toggle_class: s
} = window.__gradio__svelte__internal;
function w(i) {
  let e, t;
  return {
    c() {
      e = h("div"), t = h("iframe"), this.h();
    },
    l(l) {
      e = f(l, "DIV", { class: !0 });
      var a = d(e);
      t = f(a, "IFRAME", {
        title: !0,
        width: !0,
        height: !0,
        srcdoc: !0,
        allow: !0
      }), d(t).forEach(c), a.forEach(c), this.h();
    },
    h() {
      n(t, "title", "iframe component"), n(t, "width", "100%"), n(t, "height", "1000px"), n(
        t,
        "srcdoc",
        /*value*/
        i[0]
      ), n(t, "allow", ""), n(e, "class", "prose svelte-180qqaf"), s(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), s(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), s(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    m(l, a) {
      v(l, e, a), m(e, t);
    },
    p(l, [a]) {
      a & /*value*/
      1 && n(
        t,
        "srcdoc",
        /*value*/
        l[0]
      ), a & /*type*/
      2 && s(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), a & /*type*/
      2 && s(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), a & /*selected*/
      4 && s(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: u,
    o: u,
    d(l) {
      l && c(e);
    }
  };
}
function b(i, e, t) {
  let { value: l } = e, { type: a } = e, { selected: o = !1 } = e;
  return i.$$set = (r) => {
    "value" in r && t(0, l = r.value), "type" in r && t(1, a = r.type), "selected" in r && t(2, o = r.selected);
  }, [l, a, o];
}
class E extends _ {
  constructor(e) {
    super(), g(this, e, b, w, y, { value: 0, type: 1, selected: 2 });
  }
}
export {
  E as default
};
