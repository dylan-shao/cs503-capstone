import React from 'react';
import _ from 'lodash';
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
import Auth from '../Auth/Auth';

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {
      news: null,
      pageNum: 1,
      loadedAll: false,
    };
  }

  componentDidMount() {
    this.loadMoreNews();

    this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
    window.addEventListener('scroll', this.handleScrollY.bind(this));
  }

  handleScrollY() {
    const scrollY = window.scrollY || window.pageYOffset
      || document.documentElement.scrollTop;

    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
      this.loadMoreNews();
    }
  }

  loadMoreNews() {
    if (this.state.loadedAll === true) {
      return;
    }

    const serverUrl = location.protocol + '//' + location.host
    const url = serverUrl + '/news/userId/' + Auth.getEmail()
      + '/pageNum/' + this.state.pageNum;

    const request = new Request(encodeURI(url), {
      method: 'GET',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      },
      cache: false,
    });

    fetch(request)
      .then((res) => res.json())
      .then((returnedNews) => {
        if (!returnedNews || returnedNews.length === 0) {
          this.setState({
            loadedAll: true,
          });
        }

        this.setState({
          news: this.state.news ? this.state.news.concat(returnedNews) : returnedNews,
          pageNum: this.state.pageNum + 1,
        });
      });
  }

  renderNews() {
    const newsList = this.state.news.map((news) => {
      return (
        <a className='list-group-item' href='#'>
          <NewsCard news={news} />
        </a>
      );
    });

    return (
      <div className='container-fluid'>
        <div className='list-group'>
          {newsList}
        </div>
      </div>
    );
  }

  render() {
    if (this.state.news) {
      return (
        <div>
          {this.renderNews()}
        </div>
      );
    } else {
      return (
        <div>Loading...</div>
      );
    }
  }
}

export default NewsPanel;
