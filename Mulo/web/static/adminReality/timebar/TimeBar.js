window.addEventListener('load', async () => {
    /**
     * 主容器为 <div id="timebar"></div>
     */

class Utils {
    static clamp(start, end) {
        return function (val) {
            if (val < start) return start;
            if (val > end) return end;
            return val;
        }
    }
    static randRange(start, end) {
        return (end - start) * Math.random() + start;
    }
    static randCSSRGB() {
        return `rgb(${this.randRange(50, 200)},${this.randRange(50, 200)},${this.randRange(50, 200)})`
    }
    static str2html(str) {
        const container = document.createElement('div');
        container.innerHTML = str;
        return container.children;
    }
    static getID() {
        return Date.now().toString();
    }
}

class Target {
    flag = false;
    currentX = 0;

    /**
     * 方便在类外使用
     * @param v time
     */
    setStart(v) {
        this.start = v;
        const px = this.bar.time2px(v);
        this.updatePos(px);
    }

    /**
     *
     * @param v px
     */
    _setStart(v) {
        const time = this.bar.px2time(v);
        this.start = time;
        this.updatePos(v);
    }


    range; // time
    get end() {
        return this.start + this.range;
    }

    get width() {
        return this.bar.time2px(this.range);
    }

    /**
     *
     * @param val px
     */
    updatePos(val) {
        this.element.style.setProperty('left', `${val}px`);
    }

    /**
     * 类外使用
     * @param val time
     */
    setRange(val) {
        this.range = val
        const px = this.bar.time2px(this.range);
        this.element.style.setProperty('width', `${px}px`);
        this.updateScale();
    }

    /**
     * 类内使用
     * @param val px
     */
    _setWidth(val) {
        this.element.style.setProperty('width', `${val}px`);
    }

    /**
     * 仅 bar 更新总时长时需要调用
     */
    update() {
        this._setWidth(this.bar.time2px(this.range));
        this.updatePos(this.bar.time2px(this.start));
    }

    /**
     * 更新当前滑块的首尾刻度
     */
    updateScale() {
        const [start, end] = this.scale.children;
        start.innerHTML = this.start.toFixed(2).toString();
        end.innerHTML = this.end.toFixed(2).toString();
    }

    constructor({bar, start, range, color}) {
        this.element = document.createElement('div');
        this.hEl = document.createElement('div');
        this.bEl = document.createElement('div');
        this.tEl = document.createElement('div');
        this.hEl.innerHTML = `<div class="tri" style="border-bottom-color: ${color}"></div>`;
        this.tEl.innerHTML = `<div class="tri" style="border-bottom-color: ${color}"></div>`;
        this.element.classList.add('target');
        this.hEl.classList.add('head');
        this.bEl.classList.add('body');
        this.tEl.classList.add('tail');

        this.scale = document.createElement('div');
        this.scale.classList.add('target-scale');
        this.scale.innerHTML = `
            <div></div>
            <div></div>
        `
        this.element.append(this.hEl, this.bEl, this.tEl, this.scale);
        bar.element.appendChild(this.element);

        this.bEl.style.setProperty('background-color', color);
        this.bEl.style.setProperty('opacity', '0.5');
        this.hEl.style.setProperty('background-color', color);
        this.tEl.style.setProperty('background-color', color);

        this.bar = bar;
        this.start = start;
        this.range = range;

        this.update();
        this.updateScale();

        this.initEvent();
    }

    onMousedown = e => {
        this.flag = true;
        this.currentX = e.pageX;
        this.bar.putFirst(this);
    }
    onMouseup = () => {
        this.flag = false;
    }
    onMousemove = e => {
        e.preventDefault();
        if (this.flag) {
            const px = Utils.clamp(0, this.bar.width - this.width)(this.element.offsetLeft + e.pageX - this.currentX);
            this._setStart(px);
            this.currentX = e.pageX;
            this.updateScale();
        }
    }

    initEvent() {
        this.bEl.addEventListener('mousedown', this.onMousedown);
        document.body.addEventListener('mouseup', this.onMouseup);
        document.body.addEventListener('mousemove', this.onMousemove);
    }

    onDel() {
        this.bEl.removeEventListener('mousedown', this.onMousedown);
        this.bar.element.removeChild(this.element);
        document.body.removeEventListener('mouseup', this.onMouseup);
        document.body.removeEventListener('mousemove', this.onMousemove);
    }

    first() {
        this.element.style.setProperty('z-index', '999');
    }

    other() {
        this.element.style.setProperty('z-index', '1');
    }
}

// Odor Setting 下的单元
class Item {

    constructor(itemManager, target, {odor_id, port_id, duration, intensity, color}) {
        this.itemManager = itemManager;
        this.odor_id = odor_id;
        this.port_id = port_id;
        this.duration = duration;
        this.intensity = intensity;
        this.element = this.getPropertyItemEl({odor_id, port_id, duration, intensity, color});
        this.target = target; // 一个 Item 对应一个 Target
    }

    getPropertyItemEl({odor_id, port_id, duration, intensity, color}) {
        const {itemElTemplate, odors, ports} = this.itemManager;
        const el = itemElTemplate.cloneNode(true);
        const odorItemOdor = el.querySelector('.odor-item-odor');
        const odorItemPort = el.querySelector('.odor-item-port');
        const odorItemDuration = el.querySelector('.odor-item-duration');
        const odorItemIntensity = el.querySelector('.odor-item-intensity');
        el.querySelector('.odor-item-color').style.setProperty('background-color', color)
        odors.forEach(({id, odor}) => {
            odorItemOdor.innerHTML += `<option value="${id}" ${odor_id == id && 'selected'}>${odor}</option>`
        })
        ports.forEach(({id, port}) => {
            odorItemPort.innerHTML += `<option value="${id}" ${port_id == id && 'selected'}>${port}</option>`
        })
        odorItemDuration.value = duration;
        odorItemIntensity.value = intensity;

        const minusBtn = el.querySelector('.odor-minus-icon');

        odorItemDuration.addEventListener('change', () => {
            let temp = Number(odorItemDuration.value);
            if (temp < 0) {
                temp = 0;
                odorItemDuration.value = temp;
            } else if (temp > this.target.bar.totalTime) {
                temp = this.target.bar.totalTime;
                odorItemDuration.value = temp
            }
            this.target.setRange(temp);
        })
        minusBtn.addEventListener('click', () => {
            this.onDel();
            this.target.onDel()
        });
        return el;
    }

    onDel() {
        // TODO: 事件清理
        this.itemManager.element.removeChild(this.element);
    }
}

// class ItemElManager
class ItemManager {
    itemElStr = `
        <div class="odor-item">
            <div class="odor-item-color"></div>
            <div class="odor-item-item">
                <span class="fw-bold title">
                    Odor
                </span>
                <div class="form-group">
                    <select class="form-control bg-secondary-subtle odor-item-odor" style="border-radius: 15px;">
                        <option value="-1" selected>---------</option>
                    </select>
                </div>
            </div>
            <div class="odor-item-item">
                <span class="fw-bold title">
                    Odor Port
                </span>
                <div class="form-group">
                    <select class="form-control bg-secondary-subtle odor-item-port" style="border-radius: 15px;">
                        TODO
                    </select>
                </div>
            </div>
            <div class="odor-item-item">
                <span class="fw-bold title">
                    Duration(s)
                </span>
                <div class="form-group">
                    <input type="number" value="1" class="form-control bg-secondary-subtle odor-item-duration" style="border-radius: 15px;">
                </div>
            </div>
            <div class="odor-item-item">
                <span class="fw-bold title">
                    Intensity(%)
                </span>
                <div class="form-group">
                    <input type="number" value="1" class="form-control bg-secondary-subtle odor-item-intensity" style="border-radius: 15px;">
                </div>
            </div>
            <span class="odor-minus-icon circle-icon">-</span>
        </div>
    `

    static itemDefaultProperty = {
        odor_id: '-1',
        port_id: '1',
        duration: 3,
        intensity: 100
    };

    constructor(itemListEl, {odors, ports}) {
        this.odors = odors;
        this.ports = ports;
        this.element = itemListEl;
        this.itemElTemplate = Utils.str2html(this.itemElStr)[0];
    }

    add({
        odor_id=ItemManager.itemDefaultProperty.odor_id,
        port_id=ItemManager.itemDefaultProperty.port_id,
        duration=ItemManager.itemDefaultProperty.duration,
        intensity=ItemManager.itemDefaultProperty.intensity,
        color,
        target
    }) {
        const item = new Item(this, target,{odor_id, port_id, duration, intensity, color})
        this.element.append(item.element);
    }

    remove(item) {
        item.onDel();
    }
}

class Bar {
    tt;

    get width() {
        return this.element.clientWidth;
    }



    get time_per_px() {
        return this.width / this.totalTime;
    }


    set time_per_px(v) {
        this.time_per_px = v;
    }


    set totalTime(v) {
        this.tt = v;
        this.targets.forEach(t => {
            t.update();
        })
        this.timeScaleContainerEl.innerHTML = ''
        for (let i = 0; i <= v; i++) {
            this.timeScaleContainerEl.innerHTML += `<div>${i}</div>`
        }
    }

    get totalTime() {
        return this.tt;
    }


    constructor({el, totalTime=10, totalTimeInputEl, timeScaleContainerEl}) {
        this.targets = [];
        this.element = el;
        this.totalTimeInputEl = totalTimeInputEl;
        this.timeScaleContainerEl = timeScaleContainerEl;
        this.totalTime = totalTime;

        this.onTotalTimeInputChange();
        this.totalTimeInputEl.addEventListener('change', this.onTotalTimeInputChange);
    }

    onTotalTimeInputChange = () => {
        this.totalTime = Number(this.totalTimeInputEl.value);
    }

    add({start = 0, range=ItemManager.itemDefaultProperty.duration, color}) {
        const t = new Target({bar: this, start, range, color});
        this.targets.push(t);
        return t;
    }

    time2px(timeVal) {
        return this.time_per_px * timeVal;
    }
    px2time(pxVal) {
        return pxVal / this.time_per_px;
    }

    /**
     * 聚焦某个滑块
     * @param arg string | Target
     */
    putFirst(arg) {
        if (typeof arg === 'string') {
            this.targets.forEach(e => {
                e.id == arg ? e.first() : e.other();
            });
        } else {
            this.targets.forEach(e => {
                e.other();
            })
            arg.first();
        }
    }

    /**
     *
     * @param arg Target
     */
    remove(arg) {
        // if (typeof arg === 'string') {
        //     for (let i = 0; i < this.targets.length; i++) {
        //         if (this.targets[i].id == arg) {
        //             arg = this.targets[i];
        //             break;
        //         }
        //     }
        // }
        const _target = arg;
        _target.onDel();
        this.targets = this.targets.filter(t => t.id !== _target.id);
    }
}

    /* 初始固定数据 */
    const odors = (await (await fetch('/api/get_odor_list/')).json()).data;
    const port_choices = [
        {id: 1, port: 'Port 1'},
        {id: 2, port: 'Port 2'},
        {id: 3, port: 'Port 3'},
        {id: 4, port: 'Port 4'},
    ]
    /* 初始固定数据 */


    const targetManager = new Bar({
        el: document.getElementById('timebar'),
        totalTimeInputEl: document.querySelector('.total-time .form-group>input'),
        timeScaleContainerEl: document.querySelector('.time-scale')
    });
    const itemManager = new ItemManager(
        document.querySelector('.odor-list'),
        {odors: odors, ports: port_choices}
    )

    document.querySelector('.odor-plus-icon').addEventListener('click', () => {
        const color = Utils.randCSSRGB();
        const target = targetManager.add({start: 0 , color});
        itemManager.add({color, target});
    })
})