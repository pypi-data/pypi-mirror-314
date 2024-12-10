const {
  SvelteComponent: f,
  append_hydration: o,
  attr: u,
  children: h,
  claim_element: c,
  claim_text: y,
  detach: _,
  element: v,
  init: g,
  insert_hydration: m,
  noop: d,
  safe_not_equal: b,
  set_data: A,
  text: j,
  toggle_class: r
} = window.__gradio__svelte__internal;
function w(a) {
  let e, n = (
    /*value*/
    (a[0] ? Array.isArray(
      /*value*/
      a[0]
    ) ? (
      /*value*/
      a[0].join(", ")
    ) : (
      /*value*/
      a[0]
    ) : "") + ""
  ), i;
  return {
    c() {
      e = v("div"), i = j(n), this.h();
    },
    l(l) {
      e = c(l, "DIV", { class: !0 });
      var t = h(e);
      i = y(t, n), t.forEach(_), this.h();
    },
    h() {
      u(e, "class", "svelte-1hgn91n"), r(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), r(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), r(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    m(l, t) {
      m(l, e, t), o(e, i);
    },
    p(l, [t]) {
      t & /*value*/
      1 && n !== (n = /*value*/
      (l[0] ? Array.isArray(
        /*value*/
        l[0]
      ) ? (
        /*value*/
        l[0].join(", ")
      ) : (
        /*value*/
        l[0]
      ) : "") + "") && A(i, n), t & /*type*/
      2 && r(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), t & /*type*/
      2 && r(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), t & /*selected*/
      4 && r(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: d,
    o: d,
    d(l) {
      l && _(e);
    }
  };
}
function E(a, e, n) {
  let { value: i } = e, { type: l } = e, { selected: t = !1 } = e;
  return a.$$set = (s) => {
    "value" in s && n(0, i = s.value), "type" in s && n(1, l = s.type), "selected" in s && n(2, t = s.selected);
  }, [i, l, t];
}
class q extends f {
  constructor(e) {
    super(), g(this, e, E, w, b, { value: 0, type: 1, selected: 2 });
  }
}
export {
  q as default
};
