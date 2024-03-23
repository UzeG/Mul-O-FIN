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
    static getData(itemManager, targetManager) {
        const data = [];
        const itemData = itemManager.getData();
        const targetData = targetManager.getData();
        itemData.forEach((item, i) => {
            data.push({
                ...item,
                ...targetData[i]
            });
        });
        return data;
    }
    /**
     * 当为编辑页时需要调用。会设置时间轴长度、加载数据。
     * @param {{totalTime: number, data: {odor_id: string, port_id: string, duration: number, intensity: number, start: number}[]}} data 
     * @param {ItemManager} itemManager
     * @param {Bar} targetManager 
     */
    static loadData(itemManager, targetManager, { totalTime, data } = { totalTime: 10, data: [] }) {
        targetManager.totalTime = totalTime;
        data.forEach(({ odor_id, port_id, duration, intensity, start }) => {
            const color = Utils.randCSSRGB();
            const target = targetManager.add({ start: start, color, range: duration });
            itemManager.add({ color, target, odor_id, port_id, duration, intensity });
        });
    }

    /**
     * 
     * @param {ItemManager} itemManager 
     * @param {Bar} targetManager 
     */
    static reset(itemManager, targetManager) {
        targetManager.reset()
        itemManager.reset();
    }
}

class Target {
    flag = false;
    currentX = 0;
    /**
     * @type Item
     */
    item;

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

    setItem(item) {
        this.item = item;
    }

    constructor({ bar, start, range, color }) {
        this.id = Utils.getID();

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

        this.removeEvents = this.initEvent();
    }

    initEvent() {
        const onMousedown = e => {
            this.flag = true;
            this.currentX = e.pageX;
            this.bar.putFirst(this);
            this.item.itemManager.putFirst(this.item);
        }
        const onMouseup = () => {
            this.flag = false;
            document.body.style.setProperty('cursor', 'default');
        }
        const onMousemove = e => {
            e.preventDefault();
            if (this.flag) {
                document.body.style.setProperty('cursor', 'ew-resize');
                const px = Utils.clamp(0, this.bar.width - this.width)(this.element.offsetLeft + e.pageX - this.currentX);
                this._setStart(px);
                this.currentX = e.pageX;
                this.updateScale();
            }
        }


        this.bEl.addEventListener('mousedown', onMousedown);
        document.body.addEventListener('mouseup', onMouseup);
        document.body.addEventListener('mousemove', onMousemove);

        return () => {
            this.bEl.removeEventListener('mousedown', onMousedown);
            document.body.removeEventListener('mouseup', onMouseup);
            document.body.removeEventListener('mousemove', onMousemove);
        }
    }

    onDel() {
        this.removeEvents();
        this.bar.element.removeChild(this.element);
    }

    first() {
        this.element.classList.add('active');
    }

    other() {
        this.element.classList.remove('active');
    }

    getData() {
        return {
            start: this.start
        }
    }
}

// Odor Setting 下的单元
class Item {
    constructor(itemManager, target, { odor_id, port_id, duration, intensity, color }) {
        this.itemManager = itemManager;
        this.odor_id = odor_id;
        this.port_id = port_id;
        this.duration = duration;
        this.intensity = intensity;
        this.setPropertyItemEl({ odor_id, port_id, duration, intensity, color });
        this.removeEvents = this.initEvent();
        this.target = target; // 一个 Item 对应一个 Target
        this.id = Utils.getID();
    }

    setPropertyItemEl({ odor_id, port_id, duration, intensity, color }) {
        const { itemElTemplate, odors, ports } = this.itemManager;
        const el = itemElTemplate.cloneNode(true);
        this.element = el;
        const odorItemOdor = el.querySelector('.odor-item-odor');
        const odorItemPort = el.querySelector('.odor-item-port');
        const odorItemDuration = el.querySelector('.odor-item-duration');
        const odorItemIntensity = el.querySelector('.odor-item-intensity');
        const odorItemColor = el.querySelector('.odor-item-color');

        odors.forEach(({ id, odor }) => {
            odorItemOdor.innerHTML += `<option value="${id}" ${odor_id == id && 'selected'}>${odor}</option>`
        })
        ports.forEach(({ id, port }) => {
            odorItemPort.innerHTML += `<option value="${id}" ${port_id == id && 'selected'}>${port}</option>`
        })
        odorItemDuration.value = duration;
        odorItemIntensity.value = intensity;

        odorItemColor.style.setProperty('background-color', color);
    }

    initEvent() {
        const odorItemDuration = this.element.querySelector('.odor-item-duration');
        const minusBtn = this.element.querySelector('.odor-minus-icon');
        const odorItemColor = this.element.querySelector('.odor-item-color');
        const odorItemOdor = this.element.querySelector('.odor-item-odor');
        const odorItemPort = this.element.querySelector('.odor-item-port');
        const odorItemIntensity = this.element.querySelector('.odor-item-intensity');

        const onOdorItemDurationChange = () => {
            let temp = Number(odorItemDuration.value);
            if (temp < 0) {
                temp = 0;
                odorItemDuration.value = temp;
            } else if (temp > this.target.bar.totalTime - this.target.start) {
                temp = this.target.bar.totalTime - this.target.start;
                odorItemDuration.value = temp
            }
            this.target.setRange(temp);
            this.duration = temp;
        }

        const onMinusBtnClick = () => {
            this.target.bar.remove(this.target);
            this.itemManager.remove(this);
        }

        const onOdorItemColorClick = () => {
            this.target.bar.putFirst(this.target);
            this.itemManager.putFirst(this);
        }

        const onElementDblclick = () => {
            this.target.bar.putFirst(this.target);
            this.itemManager.putFirst(this);
        }


        const onOdorItemOdorChange = () => {
            this.odor_id = odorItemOdor.value;
        }


        const onOdorItemPortChange = () => {
            this.port_id = odorItemPort.value;
        }


        const onOdorItemIntensityChange = () => {
            this.intensity = odorItemIntensity.value;
        }


        odorItemDuration.addEventListener('change', onOdorItemDurationChange);
        minusBtn.addEventListener('click', onMinusBtnClick);
        odorItemColor.addEventListener('click', onOdorItemColorClick);
        this.element.addEventListener('dblclick', onElementDblclick);
        odorItemOdor.addEventListener('change', onOdorItemOdorChange);
        odorItemPort.addEventListener('change', onOdorItemPortChange);
        odorItemIntensity.addEventListener('change', onOdorItemIntensityChange);

        return () => {
            odorItemDuration.removeEventListener('change', onOdorItemDurationChange);
            minusBtn.removeEventListener('click', onMinusBtnClick);
            odorItemColor.removeEventListener('click', onOdorItemColorClick);
            this.element.removeEventListener('dblclick', onElementDblclick);
            odorItemOdor.removeEventListener('change', onOdorItemOdorChange);
            odorItemPort.removeEventListener('change', onOdorItemPortChange);
            odorItemIntensity.removeEventListener('change', onOdorItemIntensityChange);
        }
    }

    /**
     * 外部删除需要调用父的 remove 而不是该函数
     */
    onDel() {
        this.removeEvents();
        this.itemManager.element.removeChild(this.element);
    }

    first() {
        this.element.classList.add('active');
    }

    other() {
        this.element.classList.remove('active');
    }


    getData() {
        return {
            odor_id: this.odor_id,
            port_id: this.port_id,
            duration: this.duration,
            intensity: this.intensity
        }
    }
}

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

    constructor(itemListEl) {
        this.element = itemListEl;
        this.itemElTemplate = Utils.str2html(this.itemElStr)[0];
        this.items = [];
    }

    /**
     * ajax 方式获取 odors 和 ports 以更新 <select />
     */
    async setOdorsPosts() {
        this.odors = (await (await fetch('/api/get_odor_list/')).json()).data;
        this.ports = [
            { id: 1, port: 'Port 1' },
            { id: 2, port: 'Port 2' },
            { id: 3, port: 'Port 3' },
            { id: 4, port: 'Port 4' },
        ]
    }

    add({
        odor_id = ItemManager.itemDefaultProperty.odor_id,
        port_id = ItemManager.itemDefaultProperty.port_id,
        duration = ItemManager.itemDefaultProperty.duration,
        intensity = ItemManager.itemDefaultProperty.intensity,
        color,
        target
    }) {
        const item = new Item(this, target, { odor_id, port_id, duration, intensity, color })
        this.element.append(item.element);
        this.items.push(item);
        target.setItem(item);
    }

    remove(item) {
        item.onDel();
        this.items = this.items.filter(e => e.id !== item.id);
    }

    clear() {
        this.items.forEach(item => {
            item.onDel();
        });
        this.items.splice(0);
    }

    reset() {
        this.clear();
    }

    /**
     * 聚焦某个item
     * @param arg string | Item
     */
    putFirst(arg) {
        if (typeof arg === 'string') {
            this.items.forEach(e => {
                e.id == arg ? e.first() : e.other();
            });
        } else {
            this.items.forEach(e => {
                e.other();
            })
            arg.first();
        }
    }

    getData() {
        const data = [];
        this.items.forEach(item => {
            data.push(item.getData());
        });
        return data;
    }
}


/**
 * 主容器为 <div id="timebar"></div>
 */
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


    constructor({ el, totalTimeInputEl, timeScaleContainerEl }) {
        this.targets = [];
        this.element = el;
        this.totalTimeInputEl = totalTimeInputEl;
        this.timeScaleContainerEl = timeScaleContainerEl;

        // this.onTotalTimeInputChange();
        this.totalTimeInputEl.addEventListener('change', this.onTotalTimeInputChange);
    }

    onTotalTimeInputChange = () => {
        const temp = Number(this.totalTimeInputEl.value);
        for (const target of this.targets) {
            if (target.end > temp) {
                this.totalTimeInputEl.value = this.totalTime;
                return;
            }
        }
        this.totalTime = Number(this.totalTimeInputEl.value);
    }

    add({ start = 0, range = ItemManager.itemDefaultProperty.duration, color }) {
        const t = new Target({ bar: this, start, range, color });
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

    remove(target) {
        target.onDel();
        this.targets = this.targets.filter(t => t.id !== target.id);
    }

    clear() {
        this.targets.forEach(target => {
            target.onDel();
        });
        this.targets.splice(0);
    }

    reset() {
        this.clear();
        this.totalTime = 10;
    }

    getData() {
        const data = [];
        this.targets.forEach(item => {
            data.push(item.getData());
        });
        return data;
    }
}

/* 初始固定数据 */
// const odors = (await(await fetch('/api/get_odor_list/')).json()).data;
// const port_choices = [
//     { id: 1, port: 'Port 1' },
//     { id: 2, port: 'Port 2' },
//     { id: 3, port: 'Port 3' },
//     { id: 4, port: 'Port 4' },
// ]
/* 初始固定数据 */


// 初始化
// const targetManager = new Bar({
//     el: document.getElementById('timebar'),
//     totalTimeInputEl: document.querySelector('.total-time .form-group>input'),
//     timeScaleContainerEl: document.querySelector('.time-scale')
// });
// const itemManager = new ItemManager(
//     document.querySelector('.odor-list'),
//     { odors: odors, ports: port_choices }
// )

// 编辑时，需要请求相关的数据
// const data = [
//     {
//         "odor_id": "-1",
//         "port_id": "1",
//         "duration": 2,
//         "intensity": 100,
//         "start": 2.6802218114602585
//     },
//     {
//         "odor_id": "-1",
//         "port_id": "1",
//         "duration": 5,
//         "intensity": 100,
//         "start": 5
//     }
// ]

// Utils.loadData(data, itemManager, targetManager);

// document.querySelector('.odor-plus-icon').addEventListener('click', () => {
//     const color = Utils.randCSSRGB();
//     const target = targetManager.add({ start: 0, color });
//     itemManager.add({ color, target });
// });

// document.body.addEventListener('keydown', e => {
//     if (e.key === 'a') {
//         const data = Utils.getData(itemManager, targetManager);
//         console.log(data);
//     }
// });

// document.getElementById('btnSave').addEventListener('click', () => {
//     console.log(666)
// })
