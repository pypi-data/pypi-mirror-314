import { g as V, w as v } from "./Index-Dfp1ROHM.js";
const h = window.ms_globals.React, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.message;
var G = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) re.call(t, l) && !se.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: oe.current
  };
}
x.Fragment = ne;
x.jsx = H;
x.jsxs = H;
G.exports = x;
var w = G.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: j,
  check_outros: ie,
  children: U,
  claim_element: q,
  claim_space: ce,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: B,
  empty: T,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: J,
  space: he,
  transition_in: R,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ye,
  onDestroy: Ee,
  setContext: be
} = window.__gradio__svelte__internal;
function F(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ue(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = B("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ge(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? fe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (R(o, e), r = !0);
    },
    o(e) {
      k(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = B("react-portal-target"), r = he(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(g), r = ce(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      C(s, t, i), n[8](t), C(s, r, i), e && e.m(s, i), C(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = F(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      o || (R(e), o = !0);
    },
    o(s) {
      k(e), o = !1;
    },
    d(s) {
      s && (g(t), g(r), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ce(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = ae(e);
  let {
    svelteInit: c
  } = t;
  const f = v(M(t)), d = v();
  N(n, d, (a) => r(0, l = a));
  const _ = v();
  N(n, _, (a) => r(1, o = a));
  const u = [], m = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: S,
    subSlotIndex: y
  } = V() || {}, E = c({
    parent: m,
    props: f,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", E), we(() => {
    f.set(M(t));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function b(a) {
    j[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function Y(a) {
    j[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = L(L({}, t), A(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = A(t), [l, o, d, _, i, c, s, e, b, Y];
}
class Re extends le {
  constructor(t) {
    super(), me(this, t, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, I = window.ms_globals.tree;
function xe(n) {
  function t(r) {
    const l = v(), o = new Re({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? I;
          return i.nodes = [...i.nodes, s], W({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), W({
              createPortal: O,
              node: I
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Se.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function P(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...e]
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
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = P(e);
      t.push(...i), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const D = K(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = Q(), [s, i] = X([]);
  return z(() => {
    var _;
    if (!e.current || !n)
      return;
    let c = n;
    function f() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(o, u), r && u.classList.add(...r.split(" ")), l) {
        const m = Ie(l);
        Object.keys(m).forEach((p) => {
          u.style[p] = m[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, E, b;
        (y = e.current) != null && y.contains(c) && ((E = e.current) == null || E.removeChild(c));
        const {
          portals: p,
          clonedElement: S
        } = P(n);
        return c = S, i(p), c.style.display = "contents", f(), (b = e.current) == null || b.appendChild(c), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", f(), (_ = e.current) == null || _.appendChild(c);
    return () => {
      var u, m;
      c.style.display = "", (u = e.current) != null && u.contains(c) && ((m = e.current) == null || m.removeChild(c)), d == null || d.disconnect();
    };
  }, [n, t, r, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Pe(n, t = !1) {
  try {
    if (t && !ke(n))
      return;
    if (typeof n == "string") {
      let r = n.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Le(n, t) {
  return Z(() => Pe(n, t), [n, t]);
}
const Ne = xe(({
  slots: n,
  children: t,
  visible: r,
  onVisible: l,
  onClose: o,
  getContainer: e,
  messageKey: s,
  ...i
}) => {
  const c = Le(e), [f, d] = $.useMessage({
    ...i,
    getContainer: c
  });
  return z(() => (r ? f.open({
    ...i,
    key: s,
    icon: n.icon ? /* @__PURE__ */ w.jsx(D, {
      slot: n.icon
    }) : i.icon,
    content: n.content ? /* @__PURE__ */ w.jsx(D, {
      slot: n.content
    }) : i.content,
    onClose(..._) {
      l == null || l(!1), o == null || o(..._);
    }
  }) : f.destroy(s), () => {
    f.destroy(s);
  }), [r, s, i.content, i.className, i.duration, i.icon, i.style, i.type]), /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), d]
  });
});
export {
  Ne as Message,
  Ne as default
};
