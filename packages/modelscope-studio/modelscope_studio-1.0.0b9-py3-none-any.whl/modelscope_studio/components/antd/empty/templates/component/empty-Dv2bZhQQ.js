import { g as Z, w as b } from "./Index-j62P30nX.js";
const m = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, R = window.ms_globals.antd.Empty;
var W = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: re.current
  };
}
I.Fragment = te;
I.jsx = z;
I.jsxs = z;
W.exports = I;
var P = W.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: A,
  check_outros: le,
  children: H,
  claim_element: K,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ce,
  detach: h,
  element: q,
  empty: D,
  exclude_internal_props: j,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: V,
  space: me,
  transition_in: S,
  transition_out: k,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ge,
  onDestroy: we,
  setContext: ye
} = window.__gradio__svelte__internal;
function M(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = ce(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(t);
      o && o.l(l), l.forEach(h), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && he(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (S(o, e), r = !0);
    },
    o(e) {
      k(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function be(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      t = q("react-portal-target"), r = me(), e && e.c(), s = D(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(h), r = ie(l), e && e.l(l), s = D(), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      v(l, t, a), n[8](t), v(l, r, a), e && e.m(l, a), v(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && S(e, 1)) : (e = M(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (fe(), k(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      o || (S(e), o = !0);
    },
    o(l) {
      k(e), o = !1;
    },
    d(l) {
      l && (h(t), h(r), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function G(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ve(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = ae(e);
  let {
    svelteInit: i
  } = t;
  const E = b(G(t)), u = b();
  N(n, u, (c) => r(0, s = c));
  const p = b();
  N(n, p, (c) => r(1, o = c));
  const d = [], f = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: C,
    subSlotIndex: g
  } = Z() || {}, w = i({
    parent: f,
    props: E,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: C,
    subSlotIndex: g,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", w), Ee(() => {
    E.set(G(t));
  }), we(() => {
    d.forEach((c) => c());
  });
  function y(c) {
    A[c ? "unshift" : "push"](() => {
      s = c, u.set(s);
    });
  }
  function B(c) {
    A[c ? "unshift" : "push"](() => {
      o = c, p.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = L(L({}, t), j(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, l = c.$$scope);
  }, t = j(t), [s, o, u, p, a, i, l, e, y, B];
}
class Se extends se {
  constructor(t) {
    super(), _e(this, t, ve, be, pe, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ie(n) {
  function t(r) {
    const s = b(), o = new Se({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? x;
          return a.nodes = [...a.nodes, l], F({
            createPortal: O,
            node: x
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: O,
              node: x
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Ce.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function T(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = T(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...m.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = T(e);
      t.push(...a), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Pe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const U = J(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = Y(), [l, a] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function E() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Pe(o, d), r && d.classList.add(...r.split(" ")), s) {
        const f = Re(s);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var g, w, y;
        (g = e.current) != null && g.contains(i) && ((w = e.current) == null || w.removeChild(i));
        const {
          portals: _,
          clonedElement: C
        } = T(n);
        return i = C, a(_), i.style.display = "contents", E(), (y = e.current) == null || y.appendChild(i), _.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", E(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, r, s, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
}), Oe = Ie(({
  slots: n,
  imageStyle: t,
  ...r
}) => {
  const s = () => {
    if (n.image)
      return /* @__PURE__ */ P.jsx(U, {
        slot: n.image
      });
    switch (r.image) {
      case "PRESENTED_IMAGE_DEFAULT":
        return R.PRESENTED_IMAGE_DEFAULT;
      case "PRESENTED_IMAGE_SIMPLE":
        return R.PRESENTED_IMAGE_SIMPLE;
      default:
        return r.image;
    }
  };
  return /* @__PURE__ */ P.jsx(R, {
    ...r,
    description: n.description ? /* @__PURE__ */ P.jsx(U, {
      slot: n.description
    }) : r.description,
    imageStyle: {
      display: "inline-block",
      ...t
    },
    image: s()
  });
});
export {
  Oe as Empty,
  Oe as default
};
