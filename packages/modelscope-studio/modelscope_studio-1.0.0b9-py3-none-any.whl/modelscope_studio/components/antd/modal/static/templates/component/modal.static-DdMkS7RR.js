import { g as oe, w as I } from "./Index-CVh7hI3-.js";
const w = window.ms_globals.React, ee = window.ms_globals.React.forwardRef, q = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, J = window.ms_globals.React.useEffect, ne = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, re = window.ms_globals.antd.Modal;
var Y = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var le = w, se = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ie.call(n, l) && !ue.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: se,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: ae.current
  };
}
k.Fragment = ce;
k.jsx = Q;
k.jsxs = Q;
Y.exports = k;
var f = Y.exports;
const {
  SvelteComponent: de,
  assign: M,
  binding_callbacks: N,
  check_outros: fe,
  children: X,
  claim_element: Z,
  claim_space: _e,
  component_subscribe: W,
  compute_slots: me,
  create_slot: pe,
  detach: E,
  element: V,
  empty: D,
  exclude_internal_props: z,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: ye,
  insert_hydration: P,
  safe_not_equal: be,
  set_custom_element_data: $,
  space: xe,
  transition_in: S,
  transition_out: F,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Re,
  onDestroy: Ce,
  setContext: Ie
} = window.__gradio__svelte__internal;
function G(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = pe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = V("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = Z(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = X(n);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      $(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      P(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ee(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? ge(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (S(r, t), o = !0);
    },
    o(t) {
      F(r, t), o = !1;
    },
    d(t) {
      t && E(n), r && r.d(t), e[9](null);
    }
  };
}
function Pe(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      n = V("react-portal-target"), o = xe(), t && t.c(), l = D(), this.h();
    },
    l(s) {
      n = Z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), X(n).forEach(E), o = _e(s), t && t.l(s), l = D(), this.h();
    },
    h() {
      $(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      P(s, n, i), e[8](n), P(s, o, i), t && t.m(s, i), P(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && S(t, 1)) : (t = G(s), t.c(), S(t, 1), t.m(l.parentNode, l)) : t && (we(), F(t, 1, 1, () => {
        t = null;
      }), fe());
    },
    i(s) {
      r || (S(t), r = !0);
    },
    o(s) {
      F(t), r = !1;
    },
    d(s) {
      s && (E(n), E(o), E(l)), e[8](null), t && t.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Se(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = me(t);
  let {
    svelteInit: a
  } = n;
  const p = I(H(n)), d = I();
  W(e, d, (u) => o(0, l = u));
  const h = I();
  W(e, h, (u) => o(1, r = u));
  const c = [], _ = Re("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: v,
    subSlotIndex: y
  } = oe() || {}, b = a({
    parent: _,
    props: p,
    target: d,
    slot: h,
    slotKey: m,
    slotIndex: v,
    subSlotIndex: y,
    onDestroy(u) {
      c.push(u);
    }
  });
  Ie("$$ms-gr-react-wrapper", b), ve(() => {
    p.set(H(n));
  }), Ce(() => {
    c.forEach((u) => u());
  });
  function x(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function R(u) {
    N[u ? "unshift" : "push"](() => {
      r = u, h.set(r);
    });
  }
  return e.$$set = (u) => {
    o(17, n = M(M({}, n), z(u))), "svelteInit" in u && o(5, a = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = z(n), [l, r, d, h, i, a, s, t, x, R];
}
class ke extends de {
  constructor(n) {
    super(), ye(this, n, Se, Pe, be, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, T = window.ms_globals.tree;
function Oe(e) {
  function n(o) {
    const l = I(), r = new ke({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? T;
          return i.nodes = [...i.nodes, s], U({
            createPortal: j,
            node: T
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== l), U({
              createPortal: j,
              node: T
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Te.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function B(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(j(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = B(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...w.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: i,
      useCapture: a
    }) => {
      o.addEventListener(i, s, a);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = B(t);
      n.push(...i), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Fe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = ee(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = q(), [s, i] = te([]);
  return J(() => {
    var h;
    if (!t.current || !e)
      return;
    let a = e;
    function p() {
      let c = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (c = a.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(r, c), o && c.classList.add(...o.split(" ")), l) {
        const _ = je(l);
        Object.keys(_).forEach((m) => {
          c.style[m] = _[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var y, b, x;
        (y = t.current) != null && y.contains(a) && ((b = t.current) == null || b.removeChild(a));
        const {
          portals: m,
          clonedElement: v
        } = B(e);
        return a = v, i(m), a.style.display = "contents", p(), (x = t.current) == null || x.appendChild(a), m.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", p(), (h = t.current) == null || h.appendChild(a);
    return () => {
      var c, _;
      a.style.display = "", (c = t.current) != null && c.contains(a) && ((_ = t.current) == null || _.removeChild(a)), d == null || d.disconnect();
    };
  }, [e, n, o, l, r]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Be(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Le(e, n = !1) {
  try {
    if (n && !Be(e))
      return;
    if (typeof e == "string") {
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function C(e, n) {
  return ne(() => Le(e, n), [e, n]);
}
function Ae(e, n) {
  return e ? /* @__PURE__ */ f.jsx(g, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function K({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Ae(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ne = Oe(({
  slots: e,
  afterClose: n,
  afterOpenChange: o,
  getContainer: l,
  children: r,
  modalRender: t,
  setSlotParams: s,
  onVisible: i,
  onCancel: a,
  onOk: p,
  visible: d,
  type: h,
  ...c
}) => {
  const _ = C(o), m = C(n), v = C(l), y = C(t), [b, x] = re.useModal(), R = q(null);
  return J(() => {
    var u, L, A;
    d ? R.current = b[h || "info"]({
      ...c,
      autoFocusButton: c.autoFocusButton === void 0 ? null : c.autoFocusButton,
      afterOpenChange: _,
      afterClose: m,
      getContainer: typeof l == "string" ? v : l,
      okText: e.okText ? /* @__PURE__ */ f.jsx(g, {
        slot: e.okText
      }) : c.okText,
      okButtonProps: {
        ...c.okButtonProps || {},
        icon: e["okButtonProps.icon"] ? /* @__PURE__ */ f.jsx(g, {
          slot: e["okButtonProps.icon"]
        }) : (u = c.okButtonProps) == null ? void 0 : u.icon
      },
      cancelText: e.cancelText ? /* @__PURE__ */ f.jsx(g, {
        slot: e.cancelText
      }) : c.cancelText,
      cancelButtonProps: {
        ...c.cancelButtonProps || {},
        icon: e["cancelButtonProps.icon"] ? /* @__PURE__ */ f.jsx(g, {
          slot: e["cancelButtonProps.icon"]
        }) : (L = c.cancelButtonProps) == null ? void 0 : L.icon
      },
      closable: e["closable.closeIcon"] ? {
        ...typeof c.closable == "object" ? c.closable : {},
        closeIcon: /* @__PURE__ */ f.jsx(g, {
          slot: e["closable.closeIcon"]
        })
      } : c.closable,
      closeIcon: e.closeIcon ? /* @__PURE__ */ f.jsx(g, {
        slot: e.closeIcon
      }) : c.closeIcon,
      footer: e.footer ? K({
        slots: e,
        setSlotParams: s,
        key: "footer"
      }) : c.footer,
      title: e.title ? /* @__PURE__ */ f.jsx(g, {
        slot: e.title
      }) : c.title,
      modalRender: e.modalRender ? K({
        slots: e,
        setSlotParams: s,
        key: "modalRender"
      }) : y,
      onCancel(...O) {
        a == null || a(...O), i == null || i(!1);
      },
      onOk(...O) {
        p == null || p(...O), i == null || i(!1);
      }
    }) : ((A = R.current) == null || A.destroy(), R.current = null);
  }, [d]), /* @__PURE__ */ f.jsxs(f.Fragment, {
    children: [/* @__PURE__ */ f.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), x]
  });
});
export {
  Ne as ModalStatic,
  Ne as default
};
