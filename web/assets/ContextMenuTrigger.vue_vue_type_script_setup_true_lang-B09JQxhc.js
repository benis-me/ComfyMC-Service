import{c as D,b as v}from"./createLucideIcon-oRatMBTM.js";import{d,M as h,o as i,i as p,w as l,j as u,A as w,B,u as e,N as T,h as g,c as f,P as N,Q as R,m as y,e as _,R as S,a as A,n as $,S as j,T as q,U as K,W as L,X as C,Y as E,b as x,t as U,I as W,Z,$ as Q,q as b,a0 as X,a1 as Y,a2 as G,H as J,a3 as ee}from"./index-DugMiPrc.js";import{F as te}from"./Input.vue_vue_type_script_setup_true_lang-D1WgT5UA.js";/**
 * @license lucide-vue-next v0.341.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const me=D("ArrowRightCircleIcon",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M8 12h8",key:"1wcyev"}],["path",{d:"m12 16 4-4-4-4",key:"1i9zcv"}]]);/**
 * @license lucide-vue-next v0.341.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const fe=D("FileImageIcon",[["path",{d:"M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z",key:"1rqfz7"}],["path",{d:"M14 2v4a2 2 0 0 0 2 2h4",key:"tnqrlb"}],["circle",{cx:"10",cy:"12",r:"2",key:"737tya"}],["path",{d:"m20 17-1.296-1.296a2.41 2.41 0 0 0-3.408 0L9 22",key:"wt3hpn"}]]),se=d({__name:"AlertDialog",props:{open:{type:Boolean},defaultOpen:{type:Boolean}},emits:["update:open"],setup(a,{emit:t}){const s=h(a,t);return(m,r)=>(i(),p(e(T),w(B(e(s))),{default:l(()=>[u(m.$slots,"default")]),_:3},16))}}),ae=d({__name:"AlertDialogContent",props:{forceMount:{type:Boolean},trapFocus:{type:Boolean},disableOutsidePointerEvents:{type:Boolean},asChild:{type:Boolean},as:{},class:{}},emits:["escapeKeyDown","pointerDownOutside","focusOutside","interactOutside","openAutoFocus","closeAutoFocus"],setup(a,{emit:t}){const o=a,n=t,s=g(()=>{const{class:r,...c}=o;return c}),m=h(s,n);return(r,c)=>(i(),p(e(S),null,{default:l(()=>[f(e(N),{class:"fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"}),f(e(R),y(e(m),{class:e(_)("fixed left-1/2 top-1/2 z-50 grid w-full max-w-lg -translate-x-1/2 -translate-y-1/2 gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",o.class)}),{default:l(()=>[u(r.$slots,"default")]),_:3},16,["class"])]),_:3}))}}),oe=d({__name:"AlertDialogFooter",props:{class:{}},setup(a){const t=a;return(o,n)=>(i(),A("div",{class:$(e(_)("flex flex-col-reverse sm:flex-row sm:justify-end sm:gap-x-2",t.class))},[u(o.$slots,"default")],2))}}),ne=d({__name:"AlertDialogAction",props:{asChild:{type:Boolean},as:{},class:{}},setup(a){const t=a,o=g(()=>{const{class:n,...s}=t;return s});return(n,s)=>(i(),p(e(j),y(o.value,{class:e(_)(e(v)(),t.class)}),{default:l(()=>[u(n.$slots,"default")]),_:3},16,["class"]))}}),le=d({__name:"AlertDialogCancel",props:{asChild:{type:Boolean},as:{},class:{}},setup(a){const t=a,o=g(()=>{const{class:n,...s}=t;return s});return(n,s)=>(i(),p(e(q),y(o.value,{class:e(_)(e(v)({variant:"outline"}),"mt-2 sm:mt-0",t.class)}),{default:l(()=>[u(n.$slots,"default")]),_:3},16,["class"]))}}),re=d({__name:"AlertDialogHeader",props:{class:{}},setup(a){const t=a;return(o,n)=>(i(),A("div",{class:$(e(_)("flex flex-col gap-y-2 text-center sm:text-left",t.class))},[u(o.$slots,"default")],2))}}),ce=d({__name:"AlertDialogDescription",props:{asChild:{type:Boolean},as:{},class:{}},setup(a){const t=a,o=g(()=>{const{class:n,...s}=t;return s});return(n,s)=>(i(),p(e(K),y(o.value,{class:e(_)("text-sm text-muted-foreground",t.class)}),{default:l(()=>[u(n.$slots,"default")]),_:3},16,["class"]))}}),de=d({__name:"AlertDialogTitle",props:{asChild:{type:Boolean},as:{},class:{}},setup(a){const t=a,o=g(()=>{const{class:n,...s}=t;return s});return(n,s)=>(i(),p(e(L),y(o.value,{class:e(_)("text-lg font-semibold",t.class)}),{default:l(()=>[u(n.$slots,"default")]),_:3},16,["class"]))}}),_e=d({__name:"FlowDeleteAlert",props:C({flows:{}},{modelValue:{type:Boolean,default:!1},modelModifiers:{}}),emits:C(["onDeleted"],["update:modelValue"]),setup(a,{emit:t}){const o=a,n=t,s=E(a,"modelValue");async function m(){for(const r of o.flows)await te.delete(r.id);s.value=!1,W.success("删除成功"),n("onDeleted")}return(r,c)=>{const M=de,P=ce,k=re,F=le,z=ne,O=oe,I=ae,V=se;return i(),p(V,{open:s.value,"onUpdate:open":c[0]||(c[0]=H=>s.value=H)},{default:l(()=>[f(I,null,{default:l(()=>[f(k,null,{default:l(()=>[f(M,null,{default:l(()=>[x("删除工作流")]),_:1}),f(P,null,{default:l(()=>[x(" 确定要删除"+U(r.flows.length>1?"这些":"")+"工作流吗？删除后无法恢复。 ",1)]),_:1})]),_:1}),f(O,null,{default:l(()=>[f(F,null,{default:l(()=>[x("取消")]),_:1}),f(z,{onClick:m},{default:l(()=>[x("删除")]),_:1})]),_:1})]),_:1})]),_:1},8,["open"])}}}),ge=d({__name:"ContextMenu",props:{dir:{},modal:{type:Boolean}},emits:["update:open"],setup(a,{emit:t}){const s=h(a,t);return(m,r)=>(i(),p(e(Z),w(B(e(s))),{default:l(()=>[u(m.$slots,"default")]),_:3},16))}}),ye=d({__name:"ContextMenuContent",props:{forceMount:{type:Boolean},loop:{type:Boolean},alignOffset:{},avoidCollisions:{type:Boolean},collisionBoundary:{},collisionPadding:{},sticky:{},hideWhenDetached:{type:Boolean},prioritizePosition:{type:Boolean},asChild:{type:Boolean},as:{},class:{}},emits:["escapeKeyDown","pointerDownOutside","focusOutside","interactOutside","closeAutoFocus"],setup(a,{emit:t}){const o=a,n=t,s=g(()=>{const{class:r,...c}=o;return c}),m=h(s,n);return(r,c)=>(i(),p(e(X),null,{default:l(()=>[f(e(Q),y(e(m),{class:e(_)("z-50 min-w-32 overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",o.class),onContextmenu:c[0]||(c[0]=b(()=>{},["prevent"]))}),{default:l(()=>[u(r.$slots,"default")]),_:3},16,["class"])]),_:3}))}}),he=d({__name:"ContextMenuSeparator",props:{asChild:{type:Boolean},as:{},class:{}},setup(a){const t=a,o=g(()=>{const{class:n,...s}=t;return s});return(n,s)=>(i(),p(e(Y),y(o.value,{class:e(_)("-mx-1 my-1 h-px bg-border",t.class)}),null,16,["class"]))}}),xe=d({__name:"ContextMenuItem",props:{disabled:{type:Boolean},textValue:{},asChild:{type:Boolean},as:{},class:{},inset:{type:Boolean}},emits:["select"],setup(a,{emit:t}){const o=a,n=t,s=g(()=>{const{class:r,...c}=o;return c}),m=h(s,n);return(r,c)=>(i(),p(e(G),y(e(m),{class:e(_)("relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",r.inset&&"pl-8",o.class),onContextmenu:c[0]||(c[0]=b(()=>{},["prevent"]))}),{default:l(()=>[u(r.$slots,"default")]),_:3},16,["class"]))}}),we=d({__name:"ContextMenuTrigger",props:{disabled:{type:Boolean},asChild:{type:Boolean},as:{}},setup(a){const o=J(a);return(n,s)=>(i(),p(e(ee),w(B(e(o))),{default:l(()=>[u(n.$slots,"default")]),_:3},16))}});export{me as A,fe as F,we as _,xe as a,he as b,ye as c,ge as d,_e as e};
