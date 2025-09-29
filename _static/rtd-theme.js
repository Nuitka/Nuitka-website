function handleNav() {
  'use strict';

  const ThemeNav = {
    navBar: null,
    win: window,
    winScroll: false,
    winResize: false,
    linkScroll: false,
    winPosition: 0,
    winHeight: null,
    docHeight: null,
    isRunning: false,

    enable: function (withScroll = true) {
      const self = this;
      if (self.isRunning) return;
      self.isRunning = true;
      self.init();
      self.reset();

      window.addEventListener('hashchange', () => self.reset());

      if (withScroll) {
        window.addEventListener('scroll', () => {
          if (!self.linkScroll && !self.winScroll) {
            self.winScroll = true;
            requestAnimationFrame(() => self.onScroll());
          }
        });
      }

      window.addEventListener('resize', () => {
        if (!self.winResize) {
          self.winResize = true;
          requestAnimationFrame(() => self.onResize());
        }
      });

      self.onResize();
    },

    enableSticky: function () {
      this.enable(true);
    },

    init: function () {
      const self = this;

      this.navBar = document.querySelector('div.wy-side-scroll:first-child') ||
                    document.querySelector('div.wy-side-scroll');

      const navTopToggle = document.querySelector('[data-toggle="wy-nav-top"]');
      if (navTopToggle) {
        navTopToggle.addEventListener('click', () => {
          const navShift = document.querySelector('[data-toggle="wy-nav-shift"]');
          const rstVersions = document.querySelector('[data-toggle="rst-versions"]');
          if (navShift) navShift.classList.toggle('shift');
          if (rstVersions) rstVersions.classList.toggle('shift');

          const isOpen = navShift && navShift.classList.contains('shift');

          navTopToggle.classList.toggle('menu-open', isOpen);
        });
      }

      const menuLinks = document.querySelectorAll('.wy-menu-vertical .current ul li a');
      menuLinks.forEach(link => {
        link.addEventListener('click', function () {
          const navShift = document.querySelector('[data-toggle="wy-nav-shift"]');
          const rstVersions = document.querySelector('[data-toggle="rst-versions"]');
          if (navShift) navShift.classList.remove('shift');
          if (rstVersions) rstVersions.classList.toggle('shift');

          self.toggleCurrent(this);
          self.hashChange();
        });
      });

      const versionToggle = document.querySelector('[data-toggle="rst-current-version"]');
      if (versionToggle) {
        versionToggle.addEventListener('click', () => {
          const rstVersions = document.querySelector('[data-toggle="rst-versions"]');
          if (rstVersions) rstVersions.classList.toggle('shift-up');
        });
      }

      const tables = document.querySelectorAll(
        'table.docutils:not(.field-list):not(.footnote):not(.citation)'
      );
      tables.forEach(table => {
        if (!table.parentElement.classList.contains('wy-table-responsive')) {
          const wrapper = document.createElement('div');
          wrapper.className = 'wy-table-responsive';
          table.parentNode.insertBefore(wrapper, table);
          wrapper.appendChild(table);
        }
      });

      const footnotes = document.querySelectorAll('table.docutils.footnote');
      footnotes.forEach(table => {
        if (!table.parentElement.classList.contains('wy-table-responsive')) {
          const wrapper = document.createElement('div');
          wrapper.className = 'wy-table-responsive footnote';
          table.parentNode.insertBefore(wrapper, table);
          wrapper.appendChild(table);
        }
      });

      const citations = document.querySelectorAll('table.docutils.citation');
      citations.forEach(table => {
        if (!table.parentElement.classList.contains('wy-table-responsive')) {
          const wrapper = document.createElement('div');
          wrapper.className = 'wy-table-responsive citation';
          table.parentNode.insertBefore(wrapper, table);
          wrapper.appendChild(table);
        }
      });

      const menuItems = document.querySelectorAll('.wy-menu-vertical ul:not(.simple)');
      menuItems.forEach(ul => {
        const sibling = ul.previousElementSibling;
        if (sibling && sibling.tagName === 'A' && !sibling.querySelector('.toctree-expand')) {
          const expand = document.createElement('button');
          expand.className = 'toctree-expand';
          expand.title = 'Open/close menu';
          expand.addEventListener('click', e => {
            e.stopPropagation();
            self.toggleCurrent(sibling);
            return false;
          });
          sibling.insertBefore(expand, sibling.firstChild);
        }
      });
    },

    reset: function () {
      const anchor = encodeURI(window.location.hash) || '#';
      try {
        const menu = document.querySelector('.wy-menu-vertical');
        if (!menu) return;

        let link = menu.querySelector(`a[href="${anchor}"]`);
        if (!link) {
          const anchorId = anchor.substring(1);
          const section = document.querySelector(`.document [id="${anchorId}"]`);
          if (section) {
            const closestSection = section.closest('div.section');
            if (closestSection) {
              link = menu.querySelector(`a[href="#${closestSection.getAttribute('id')}"]`);
            }
          }
          if (!link) link = menu.querySelector('a[href="#"]');
        }

        if (link) {
          const currentItems = menu.querySelectorAll('.current');
          currentItems.forEach(item => {
            item.classList.remove('current');
            item.setAttribute('aria-expanded', 'false');
          });

          link.classList.add('current');
          link.setAttribute('aria-expanded', 'true');

          const parentLi = link.closest('li.toctree-l1');
          if (parentLi && parentLi.parentElement) {
            parentLi.parentElement.classList.add('current');
            parentLi.parentElement.setAttribute('aria-expanded', 'true');
          }

          for (let i = 1; i <= 10; i++) {
            const parent = link.closest(`li.toctree-l${i}`);
            if (parent) {
              parent.classList.add('current');
              parent.setAttribute('aria-expanded', 'true');
            }
          }

          link.scrollIntoView();
        }
      } catch (err) {
        console.log('Error expanding nav for anchor', err);
      }
    },

    onScroll: function () {
      this.winScroll = false;
      const newWinPosition = window.pageYOffset;
      const winBottom = newWinPosition + this.winHeight;
      const navPosition = this.navBar.scrollTop + (newWinPosition - this.winPosition);

      if (newWinPosition < 0 || winBottom > this.docHeight) return;
      this.navBar.scrollTop = navPosition;
      this.winPosition = newWinPosition;
    },

    onResize: function () {
      this.winResize = false;
      this.winHeight = window.innerHeight;
      this.docHeight = document.documentElement.scrollHeight;
    },

    hashChange: function () {
      this.linkScroll = true;
      const self = this;
      window.addEventListener(
        'hashchange',
        function handler() {
          self.linkScroll = false;
          window.removeEventListener('hashchange', handler);
        },
        { once: true }
      );
    },

    toggleCurrent: function (element) {
      const link = element.tagName === 'A' ? element : element.querySelector('a');
      if (!link) return;

      const li = link.closest('li');
      if (!li) return;

      const siblings = Array.from(li.parentElement.children).filter(
        el => el !== li && el.tagName === 'LI'
      );
      siblings.forEach(sibling => {
        sibling.classList.remove('current');
        sibling.setAttribute('aria-expanded', 'false');
        const subCurrents = sibling.querySelectorAll('li.current');
        subCurrents.forEach(subCurrent => {
          subCurrent.classList.remove('current');
          subCurrent.setAttribute('aria-expanded', 'false');
        });
      });

      const subUl = li.querySelector(':scope > ul');
      if (subUl) {
        const subLis = subUl.querySelectorAll(':scope > li');
        subLis.forEach(subLi => {
          subLi.classList.remove('current');
          subLi.setAttribute('aria-expanded', 'false');
        });
        const isExpanded = li.getAttribute('aria-expanded') === 'true';
        li.classList.toggle('current');
        li.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
      }
    }
  };

  if (typeof window !== 'undefined') {
    window.SphinxRtdTheme = { Navigation: ThemeNav, StickyNav: ThemeNav };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ThemeNav.enable());
  } else {
    ThemeNav.enable();
  }

  // Polyfill for requestAnimationFrame
  (() => {
    let lastTime = 0;
    const vendors = ['ms', 'moz', 'webkit', 'o'];
    for (let x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
      window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
      window.cancelAnimationFrame =
        window[vendors[x] + 'CancelAnimationFrame'] ||
        window[vendors[x] + 'CancelRequestAnimationFrame'];
    }
    if (!window.requestAnimationFrame) {
      window.requestAnimationFrame = callback => {
        const currTime = new Date().getTime();
        const timeToCall = Math.max(0, 16 - (currTime - lastTime));
        const id = window.setTimeout(() => callback(currTime + timeToCall), timeToCall);
        lastTime = currTime + timeToCall;
        return id;
      };
    }
    if (!window.cancelAnimationFrame) {
      window.cancelAnimationFrame = id => clearTimeout(id);
    }
  })();
}

handleNav();
