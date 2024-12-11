import { each, keys, get, uniqBy } from 'lodash';

export const StorageUtils = {
    remove: function (key) {
        localStorage.removeItem(key);
    },
    has: function (key) {
        return localStorage.hasOwnProperty(key);
    },
    save: function (key, item) {
            if (typeof key !== 'string') key = key.toString();
            if (typeof item !== 'string') item = JSON.stringify(item);

            localStorage.setItem(key, item);
    },
    get: function (key, defaultValue) {
        let item = localStorage.getItem(key);

        if (item !== null) {
            try { item = JSON.parse(item); } catch (e) { }
        }

        if (item === null && defaultValue !== undefined) {
            return defaultValue;
        }

        return item;
    },
    getApps: function () {
        return keys(localStorage)
                .filter(k => k.includes('cfs.app-'))
                .map(id => this.get(id));
    },
    getHomeApps: function () {
        return keys(localStorage)
                .filter(k => k.includes('cfs.app-'))
                .map(id => this.get(id))
                .filter(app => app.state === 'home');
    },
    getAppsByPath: function (path) {
        return keys(localStorage)
                .filter(k => k.includes('cfs.app-'))
                .map(id => this.get(id))
                .filter(app => app.folderPath === path);
    },
    getAppsByName: function (name, exactName = false) {
        return keys(localStorage)
                .filter(k => k.includes('cfs.app-'))
                .map(id => this.get(id))
                .filter(app => ['home', 'favorite'].includes(app.state) && (
                    (exactName && app.name.toLowerCase() === name.toLowerCase()) ||
                    (!exactName && app.name.toLowerCase().includes(name.toLowerCase()))
                ));
    },
    getAll: function () {
        const items = {};

        each(keys(localStorage), key => {
            if (key.includes('cfs.')) {
                items[key] = this.get(key);
            }
        });

        return items;
    }
};

export const getProvidersFromApp = app => {
    const providers = StorageUtils.get('cfs.dataProviders');
    const usedDataProvidersNames = uniqBy(app.widgetList
        .map(w => get(w, 'source.provider.name', null))
        .filter(pname => pname));
    const usedDataProviders = providers.filter(v => {
        if (usedDataProvidersNames.includes(v.name)) {
            if (v.customCode) delete v.customCode;
            if (v.metadata) delete v.metadata;
            return true;
        }
        return false;
    });

    return usedDataProviders;
};
