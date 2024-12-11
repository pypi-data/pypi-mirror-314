import { g as $, w as x, d as ee, a as b } from "./Index-CjmGN--A.js";
const _ = window.ms_globals.React, G = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Spin;
var K = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = _, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: le.current
  };
}
C.Fragment = re;
C.jsx = V;
C.jsxs = V;
K.exports = C;
var h = K.exports;
const {
  SvelteComponent: ae,
  assign: T,
  binding_callbacks: j,
  check_outros: ce,
  children: q,
  claim_element: B,
  claim_space: de,
  component_subscribe: A,
  compute_slots: ue,
  create_slot: fe,
  detach: g,
  element: J,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: S,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: we,
  transition_in: I,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function F(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = fe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = q(t);
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      S(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && be(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (I(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && g(t), r && r.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = J("react-portal-target"), o = we(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(g), o = de(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      S(l, t, a), n[8](t), S(l, o, a), e && e.m(l, a), S(l, s, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && I(e, 1)) : (e = F(l), e.c(), I(e, 1), e.m(s.parentNode, s)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      r || (I(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (g(t), g(o), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ie(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = ue(e);
  let {
    svelteInit: i
  } = t;
  const w = x(M(t)), u = x();
  A(n, u, (c) => o(0, s = c));
  const m = x();
  A(n, m, (c) => o(1, r = c));
  const d = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: w,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y,
    onDestroy(c) {
      d.push(c);
    }
  });
  xe("$$ms-gr-react-wrapper", E), ye(() => {
    w.set(M(t));
  }), ve(() => {
    d.forEach((c) => c());
  });
  function v(c) {
    j[c ? "unshift" : "push"](() => {
      s = c, u.set(s);
    });
  }
  function Q(c) {
    j[c ? "unshift" : "push"](() => {
      r = c, m.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = T(T({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, l = c.$$scope);
  }, t = D(t), [s, r, u, m, a, i, l, e, v, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Ie, Se, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const s = x(), r = new Ce({
      ...o,
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
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, l], W({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), W({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Oe(n) {
  const [t, o] = U(() => b(n));
  return H(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = G(() => ee(n, (o) => o), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !ke.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function L(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((r) => {
        if (_.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = L(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: l,
            children: [..._.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(e);
      t.push(...a), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Te(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const z = X(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = Z(), [l, a] = U([]);
  return H(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Te(r, d), o && d.classList.add(...o.split(" ")), s) {
        const f = Le(s);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = L(n);
        return i = R, a(p), i.style.display = "contents", w(), (v = e.current) == null || v.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, s, r]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n, t) {
  const o = G(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = b(e.props.node.slotIndex) || 0, i = b(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(l.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(o);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...o
}) => {
  const s = je(t);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: s.length === 0 ? t : null
    }), /* @__PURE__ */ h.jsx(te, {
      ...o,
      tip: n.tip ? /* @__PURE__ */ h.jsx(z, {
        slot: n.tip
      }) : o.tip,
      indicator: n.indicator ? /* @__PURE__ */ h.jsx(z, {
        slot: n.indicator
      }) : o.indicator,
      children: s.length === 0 ? void 0 : t
    })]
  });
});
export {
  Ne as Spin,
  Ne as default
};
