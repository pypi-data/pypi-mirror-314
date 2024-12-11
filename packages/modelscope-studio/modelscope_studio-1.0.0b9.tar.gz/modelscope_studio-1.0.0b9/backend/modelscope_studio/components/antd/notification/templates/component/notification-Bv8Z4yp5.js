import { g as Z, w as x } from "./Index-B0dt1yYG.js";
const g = window.ms_globals.React, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, P = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.notification;
var G = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $ = g, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ne.call(n, l) && !re.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ee,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: oe.current
  };
}
R.Fragment = te;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var p = G.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: N,
  check_outros: le,
  children: M,
  claim_element: q,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: ce,
  create_slot: ae,
  detach: w,
  element: B,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: I,
  safe_not_equal: me,
  set_custom_element_data: J,
  space: he,
  transition_in: C,
  transition_out: k,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = ae(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = B("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = M(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      I(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && pe(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
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
      r || (C(o, e), r = !0);
    },
    o(e) {
      k(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function Ee(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      n = B("react-portal-target"), r = he(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      n = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(n).forEach(w), r = ie(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      I(s, n, a), t[8](n), I(s, r, a), e && e.m(s, a), I(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = F(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (fe(), k(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      k(e), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function H(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function ve(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const a = ce(e);
  let {
    svelteInit: c
  } = n;
  const m = x(H(n)), i = x();
  T(t, i, (u) => r(0, l = u));
  const f = x();
  T(t, f, (u) => r(1, o = u));
  const d = [], _ = we("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: S,
    subSlotIndex: y
  } = Z() || {}, E = c({
    parent: _,
    props: m,
    target: i,
    slot: f,
    slotKey: h,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(u) {
      d.push(u);
    }
  });
  ye("$$ms-gr-react-wrapper", E), ge(() => {
    m.set(H(n));
  }), be(() => {
    d.forEach((u) => u());
  });
  function v(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, i.set(l);
    });
  }
  function Y(u) {
    N[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return t.$$set = (u) => {
    r(17, n = L(L({}, n), D(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, n = D(n), [l, o, i, f, a, c, s, e, v, Y];
}
class xe extends se {
  constructor(n) {
    super(), _e(this, n, ve, Ee, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ie(t) {
  function n(r) {
    const l = x(), o = new xe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, s], W({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== l), W({
              createPortal: P,
              node: O
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
      r(n);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Ce.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function j(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(P(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: g.Children.toArray(t._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...g.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = j(e);
      n.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Se(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const b = K(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Q(), [s, a] = X([]);
  return z(() => {
    var f;
    if (!e.current || !t)
      return;
    let c = t;
    function m() {
      let d = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (d = c.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Se(o, d), r && d.classList.add(...r.split(" ")), l) {
        const _ = Re(l);
        Object.keys(_).forEach((h) => {
          d.style[h] = _[h];
        });
      }
    }
    let i = null;
    if (n && window.MutationObserver) {
      let d = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(c) && ((E = e.current) == null || E.removeChild(c));
        const {
          portals: h,
          clonedElement: S
        } = j(t);
        return c = S, a(h), c.style.display = "contents", m(), (v = e.current) == null || v.appendChild(c), h.length > 0;
      };
      d() || (i = new window.MutationObserver(() => {
        d() && (i == null || i.disconnect());
      }), i.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var d, _;
      c.style.display = "", (d = e.current) != null && d.contains(c) && ((_ = e.current) == null || _.removeChild(c)), i == null || i.disconnect();
    };
  }, [t, n, r, l, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Pe = Ie(({
  slots: t,
  bottom: n,
  rtl: r,
  stack: l,
  top: o,
  children: e,
  visible: s,
  notificationKey: a,
  onClose: c,
  onVisible: m,
  ...i
}) => {
  const [f, d] = V.useNotification({
    bottom: n,
    rtl: r,
    stack: l,
    top: o
  });
  return z(() => (s ? f.open({
    ...i,
    key: a,
    btn: t.btn ? /* @__PURE__ */ p.jsx(b, {
      slot: t.btn
    }) : i.btn,
    closeIcon: t.closeIcon ? /* @__PURE__ */ p.jsx(b, {
      slot: t.closeIcon
    }) : i.closeIcon,
    description: t.description ? /* @__PURE__ */ p.jsx(b, {
      slot: t.description
    }) : i.description,
    message: t.message ? /* @__PURE__ */ p.jsx(b, {
      slot: t.message
    }) : i.message,
    icon: t.icon ? /* @__PURE__ */ p.jsx(b, {
      slot: t.icon
    }) : i.icon,
    onClose(..._) {
      m == null || m(!1), c == null || c(..._);
    }
  }) : f.destroy(a), () => {
    f.destroy(a);
  }), [s, a, i.btn, i.closeIcon, i.className, i.description, i.duration, i.showProgress, i.pauseOnHover, i.icon, i.message, i.placement, i.style, i.role, i.props]), /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [e, d]
  });
});
export {
  Pe as Notification,
  Pe as default
};
