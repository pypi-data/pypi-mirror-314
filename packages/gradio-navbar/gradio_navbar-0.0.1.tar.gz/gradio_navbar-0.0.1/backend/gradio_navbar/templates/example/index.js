const {
  SvelteComponent: z,
  add_iframe_resize_listener: E,
  add_render_callback: S,
  append_hydration: q,
  attr: C,
  binding_callbacks: D,
  children: I,
  claim_element: M,
  claim_text: P,
  detach: o,
  element: V,
  init: W,
  insert_hydration: j,
  noop: v,
  safe_not_equal: x,
  set_data: A,
  text: B,
  toggle_class: a
} = window.__gradio__svelte__internal, { onMount: F } = window.__gradio__svelte__internal;
function G(n) {
  let e, t = (
    /*value*/
    (n[0] ? (
      /*value*/
      n[0].company_name
    ) : "") + ""
  ), s, d;
  return {
    c() {
      e = V("div"), s = B(t), this.h();
    },
    l(i) {
      e = M(i, "DIV", { class: !0 });
      var _ = I(e);
      s = P(_, t), _.forEach(o), this.h();
    },
    h() {
      C(e, "class", "svelte-84cxb8"), S(() => (
        /*div_elementresize_handler*/
        n[13].call(e)
      )), a(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), a(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), a(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    m(i, _) {
      j(i, e, _), q(e, s), d = E(
        e,
        /*div_elementresize_handler*/
        n[13].bind(e)
      ), n[14](e);
    },
    p(i, [_]) {
      _ & /*value*/
      1 && t !== (t = /*value*/
      (i[0] ? (
        /*value*/
        i[0].company_name
      ) : "") + "") && A(s, t), _ & /*type*/
      2 && a(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), _ & /*type*/
      2 && a(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), _ & /*selected*/
      4 && a(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    i: v,
    o: v,
    d(i) {
      i && o(e), d(), n[14](null);
    }
  };
}
function H(n, e) {
  n.style.setProperty("--local-text-width", `${e && e < 150 ? e : 200}px`), n.style.whiteSpace = "unset";
}
function J(n, e, t) {
  let { value: s } = e, { type: d } = e, { selected: i = !1 } = e, _, c;
  F(() => {
    H(c, _);
  });
  let { visible: f = !0 } = e, { elem_id: u = null } = e, { elem_classes: m = [] } = e, { render: r = !0 } = e, { key: y = null } = e, { samples_dir: h = null } = e, { index: b = null } = e, { root: g = null } = e;
  function k() {
    _ = this.clientWidth, t(3, _);
  }
  function w(l) {
    D[l ? "unshift" : "push"](() => {
      c = l, t(4, c);
    });
  }
  return n.$$set = (l) => {
    "value" in l && t(0, s = l.value), "type" in l && t(1, d = l.type), "selected" in l && t(2, i = l.selected), "visible" in l && t(5, f = l.visible), "elem_id" in l && t(6, u = l.elem_id), "elem_classes" in l && t(7, m = l.elem_classes), "render" in l && t(8, r = l.render), "key" in l && t(9, y = l.key), "samples_dir" in l && t(10, h = l.samples_dir), "index" in l && t(11, b = l.index), "root" in l && t(12, g = l.root);
  }, [
    s,
    d,
    i,
    _,
    c,
    f,
    u,
    m,
    r,
    y,
    h,
    b,
    g,
    k,
    w
  ];
}
class K extends z {
  constructor(e) {
    super(), W(this, e, J, G, x, {
      value: 0,
      type: 1,
      selected: 2,
      visible: 5,
      elem_id: 6,
      elem_classes: 7,
      render: 8,
      key: 9,
      samples_dir: 10,
      index: 11,
      root: 12
    });
  }
}
export {
  K as default
};
