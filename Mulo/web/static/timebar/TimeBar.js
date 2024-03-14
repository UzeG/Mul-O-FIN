window.addEventListener('load', () => {
    /**
     * 主容器为 <div id="timebar"></div>
     */

    var Utils = /** @class */ (function () {
        function Utils() {
        }
        Utils.clamp = function (start, end) {
            return function (val) {
                if (val < start)
                    return start;
                if (val > end)
                    return end;
                return val;
            };
        };
        return Utils;
    }());

    var Bar = /** @class */ (function () {
        function Bar(_a, val) {
            var element = _a.element, totalTime = _a.totalTime;
            if (val === void 0) { val = 10; }
            this.targets = [];
            this.element = element;
            this.totalTime = totalTime;
            this.totalTime = val;
        }
        Object.defineProperty(Bar.prototype, "width", {
            get: function () {
                return this.element.clientWidth;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Bar.prototype, "time_per_px", {
            get: function () {
                return this.width / this.totalTime;
            },
            set: function (v) {
                this.time_per_px = v;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Bar.prototype, "totalTime", {
            get: function () {
                return this.tt;
            },
            set: function (v) {
                this.tt = v;
                this.targets.forEach(function (t) {
                    t.update();
                });
            },
            enumerable: false,
            configurable: true
        });
        Bar.prototype.add = function (start, range) {
            var t = new Target(this, start, range);
            this.targets.push(t);
            return t;
        };
        Bar.prototype.time2px = function (timeVal) {
            return this.time_per_px * timeVal;
        };
        Bar.prototype.px2time = function (pxVal) {
            return pxVal / this.time_per_px;
        };
        Bar.prototype.putFirst = function (arg) {
            if (typeof arg === 'string') {
                this.targets.forEach(function (e) {
                    e.id == arg ? e.first() : e.other();
                });
            }
            else {
                this.targets.forEach(function (e) {
                    e.other();
                });
                arg.first();
            }
        };
        Bar.prototype.removeTarget = function (arg) {
            if (typeof arg === 'string') {
                for (var i = 0; i < this.targets.length; i++) {
                    if (this.targets[i].id == arg) {
                        arg = this.targets[i];
                        break;
                    }
                }
            }
            var _target = arg;
            _target.onDel();
            this.targets = this.targets.filter(function (t) { return t.id !== _target.id; });
        };
        return Bar;
    }());

    var Target = /** @class */ (function () {
        function Target(bar, start, range) {
            this.flag = false;
            this.currentX = 0;
            this.element = document.createElement('div');
            this.hEl = document.createElement('div');
            this.bEl = document.createElement('div');
            this.tEl = document.createElement('div');
            this.element.classList.add('target');
            this.hEl.classList.add('head');
            this.bEl.classList.add('body');
            this.tEl.classList.add('tail');
            this.id = Date.now().toString();
            this.bar = bar;
            this.start = start;
            this.range = range;
            this.update();
            this.element.append(this.hEl, this.bEl, this.tEl);
            this.bar.element.appendChild(this.element);
            this.initEvent();
        }
        /**
         * 方便在类外使用
         * @param v time
         */
        Target.prototype.setStart = function (v) {
            this.start = v;
            var px = this.bar.time2px(v);
            this.updatePos(px);
        };
        /**
         *
         * @param v px
         */
        Target.prototype._setStart = function (v) {
            var time = this.bar.px2time(v);
            this.start = time;
            this.updatePos(v);
        };
        Object.defineProperty(Target.prototype, "end", {
            get: function () {
                return this.start + this.range;
            },
            enumerable: false,
            configurable: true
        });
        Object.defineProperty(Target.prototype, "width", {
            get: function () {
                return this.bar.time2px(this.range);
            },
            enumerable: false,
            configurable: true
        });
        /**
         *
         * @param val px
         */
        Target.prototype.updatePos = function (val) {
            this.element.style.setProperty('left', "".concat(val, "px"));
        };
        /**
         *
         * @param val px
         */
        Target.prototype.updateWidth = function (val) {
            this.element.style.setProperty('width', "".concat(val, "px"));
        };
        /**
         * 仅 bar 更新总时长时需要调用
         */
        Target.prototype.update = function () {
            this.updateWidth(this.bar.time2px(this.range));
            this.updatePos(this.bar.time2px(this.start));
        };
        Target.prototype.onMousedown = function (e) {
            this.flag = true;
            this.currentX = e.pageX;
            this.bar.putFirst(this);
        };
        Target.prototype.onMouseup = function () {
            this.flag = false;
        };
        Target.prototype.onMousemove = function (e) {
            e.preventDefault();
            if (this.flag) {
                var px = Utils.clamp(0, this.bar.width - this.width)(this.element.offsetLeft + e.pageX - this.currentX);
                this._setStart(px);
                this.currentX = e.pageX;
            }
        };
        Target.prototype.initEvent = function () {
            var _this = this;
            var flag = false;
            var currentX;
            var onMousedown = function (e) {
                flag = true;
                currentX = e.pageX;
                _this.bar.putFirst(_this);
            };
            var onMouseup = function () {
                flag = false;
            };
            var onMousemove = function (e) {
                e.preventDefault();
                if (flag) {
                    var px = Utils.clamp(0, _this.bar.width - _this.width)(_this.element.offsetLeft + e.pageX - currentX);
                    _this._setStart(px);
                    currentX = e.pageX;
                }
            };
            this.bEl.addEventListener('mousedown', onMousedown);
            document.body.addEventListener('mouseup', onMouseup);
            document.body.addEventListener('mousemove', onMousemove);
        };
        Target.prototype.onDel = function () {
            this.bEl.removeEventListener('mousedown', this.onMousedown);
            this.bar.element.removeChild(this.element);
            document.body.removeEventListener('mouseup', this.onMouseup);
            document.body.removeEventListener('mousemove', this.onMousemove);
        };
        Target.prototype.first = function () {
            this.element.style.setProperty('z-index', '999');
        };
        Target.prototype.other = function () {
            this.element.style.setProperty('z-index', '1');
        };
        return Target;
    }());

    const barEl = document.getElementById('timebar')
    const bar = new Bar({
        element: barEl,
        totalTime: 10
    }, 50)
    bar.add(10, 20)
})