# coding=utf-8

import collections
WILDCARD = '*'


class Sfsm(object):
    def __init__(self, cfg={},
                 initial=None, events=None, callbacks=None, final=None):
        cfg = dict(cfg)
        if "events" not in cfg:
            cfg["events"] = []
        if "callbacks" not in cfg:
            cfg["callbacks"] = {}
        if initial:
            cfg["initial"] = initial
        if final:
            cfg["final"] = final
        if events:
            cfg["events"].extend(list(events))
        if callbacks:
            cfg["callbacks"].update(dict(callbacks))
        events_dicts = []
        for e in cfg["events"]:
            if isinstance(e, collections.Mapping):
                events_dicts.append(e)
            elif hasattr(e, "__iter__"):
                name, src, dst = list(e)[:3]
                events_dicts.append({"name": name, "src": src, "dst": dst})
        cfg["events"] = events_dicts
        self._apply(cfg)

    def isstate(self, state):
        return self.current == state

    def can(self, event):
        return (event in self._map and ((self.current in self._map[event]) or WILDCARD in self._map[event])
                and not hasattr(self, 'transition'))

    def cannot(self, event):
        return not self.can(event)

    def is_finished(self):
        return self._final and (self.current == self._final)

    def _apply(self, cfg):
        init = cfg['initial'] if 'initial' in cfg else None
        if self._is_base_string(init):
            init = {'state': init}

        self._final = cfg['final'] if 'final' in cfg else None

        events = cfg['events'] if 'events' in cfg else []
        callbacks = cfg['callbacks'] if 'callbacks' in cfg else {}
        tmap = {}
        self._map = tmap

        def add(e):
            if 'src' in e:
                src = [e['src']] if self._is_base_string(
                    e['src']) else e['src']
            else:
                src = [WILDCARD]
            if e['name'] not in tmap:
                tmap[e['name']] = {}
            for s in src:
                tmap[e['name']][s] = e['dst']

        if init:
            if 'event' not in init:
                init['event'] = 'startup'
            add({'name': init['event'], 'src': 'none', 'dst': init['state']})

        for e in events:
            add(e)

        for name in tmap:
            setattr(self, name, self._build_event(name))

        for name in callbacks:
            setattr(self, name, callbacks[name])

        self.current = 'none'

        if init and 'defer' not in init:
            getattr(self, init['event'])()

    def _build_event(self, event):
        def fn(*args, **kwargs):

            if hasattr(self, 'transition'):
                raise "event %s inappropriate because previous transition did not complete" % event

            if not self.can(event):
                raise "event %s inappropriate in current state %s" % (event, self.current)

            src = self.current
            dst = ((src in self._map[event] and self._map[event][src]) or
                   WILDCARD in self._map[event] and self._map[event][WILDCARD])

            class _e_obj(object):
                pass
            e = _e_obj()
            e.fsm, e.event, e.src, e.dst = self, event, src, dst
            for k in kwargs:
                setattr(e, k, kwargs[k])

            setattr(e, 'args', args)

            if self._before_event(e) is False:
                return

            if self.current != dst:
                def _tran():
                    delattr(self, 'transition')
                    self.current = dst
                    self._enter_state(e)
                    self._change_state(e)
                    self._after_event(e)
                self.transition = _tran
            else:
                self._after_event(e)

            if self._leave_state(e) is not False:
                if hasattr(self, 'transition'):
                    self.transition()

        fn.__name__ = event
        fn.__doc__ = ("Event handler for an {event} event. This event can be " +
                      "fired if the machine is in {states} states.".format(
                          event=event, states=self._map[event].keys()))

        return fn

    def _before_event(self, e):
        fnname = 'onbefore' + e.event
        if hasattr(self, fnname):
            return getattr(self, fnname)(e)

    def _after_event(self, e):
        for fnname in ['onafter' + e.event]:
            if hasattr(self, fnname):
                return getattr(self, fnname)(e)

    def _leave_state(self, e):
        fnname = 'onleave' + e.src
        if hasattr(self, fnname):
            return getattr(self, fnname)(e)

    def _enter_state(self, e):
        for fnname in ['onenter' + e.dst]:
            if hasattr(self, fnname):
                return getattr(self, fnname)(e)

    def _change_state(self, e):
        fnname = 'onchangestate'
        if hasattr(self, fnname):
            return getattr(self, fnname)(e)

    def _is_base_string(self, object):
        try:
            return isinstance(object, basestring)
        except NameError:
            return isinstance(object, str)

    def trigger(self, event, *args, **kwargs):
        if not hasattr(self, event):
            raise "There isn't any event registered as %s" % event
        return getattr(self, event)(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        fnname = 'on' + self.current
        if hasattr(self, fnname):
            return getattr(self, fnname)(*args, **kwargs)
