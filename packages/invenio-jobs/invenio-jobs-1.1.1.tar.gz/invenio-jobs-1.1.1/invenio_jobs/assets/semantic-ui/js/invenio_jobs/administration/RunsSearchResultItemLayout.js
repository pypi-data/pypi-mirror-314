/*
 * This file is part of Invenio.
 * Copyright (C) 2024 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { NotificationContext } from "@js/invenio_administration";
import { i18next } from "@translations/invenio_jobs/i18next";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { UserListItemCompact } from "react-invenio-forms";
import { withState } from "react-searchkit";
import { Table } from "semantic-ui-react";
import { StatusFormatter } from "./StatusFormatter";
import { StopButton } from "./StopButton";
import { diffTimestamps } from "./utils/diffTimestamps";

class SearchResultItemComponent extends Component {
  constructor(props) {
    super(props);

    this.state = {
      status: props.result.status,
    };
  }

  static contextType = NotificationContext;

  onError = (e) => {
    const { addNotification } = this.context;
    addNotification({
      title: i18next.t("Status ") + e.status,
      content: `${e.message}`,
      type: "error",
    });
    console.error(e);
  };

  render() {
    const { result } = this.props;
    const { status } = this.state;
    return (
      <Table.Row>
        <Table.Cell
          key={`run-name-${result.started_at}`}
          data-label={i18next.t("Run")}
          collapsing
          className="word-break-all"
        >
          <StatusFormatter status={status} />
          <a href={result.links.self}>{result.created.slice(0, 16)}</a>
        </Table.Cell>
        <Table.Cell
          key={`run-last-run-${status}`}
          data-label={i18next.t("Duration")}
          collapsing
          className=""
        >
          {result.started_at === null
            ? `${i18next.t("Waiting")}...`
            : [
                result.finished_at === null
                  ? `${diffTimestamps(
                      new Date().toISOString(),
                      result.started_at,
                      i18next.language
                    )}...`
                  : diffTimestamps(
                      result.finished_at,
                      result.started_at,
                      i18next.language
                    ),
              ]}
        </Table.Cell>
        <Table.Cell
          key={`run-last-run-${result.message}`}
          data-label={i18next.t("Message")}
          collapsing
          className=""
        >
          {result.message}
        </Table.Cell>
        {result.started_by ? (
          <Table.Cell
            key={`job-user-${result.started_by.id}`}
            data-label={i18next.t("Started by")}
            collapsing
            className="word-break-all"
          >
            <UserListItemCompact
              user={result.started_by}
              id={result.started_by.id}
            />
          </Table.Cell>
        ) : (
          <Table.Cell
            key="job-user"
            data-label={i18next.t("Started by")}
            collapsing
            className="word-break-all"
          >
            System
          </Table.Cell>
        )}
        <Table.Cell collapsing>
          {status === "RUNNING" ? (
            <StopButton
              stopURL={result.links.stop}
              setStatus={(status) => {
                this.setState({ status: status });
              }}
              onError={this.onError}
            />
          ) : (
            ""
          )}
        </Table.Cell>
      </Table.Row>
    );
  }
}

SearchResultItemComponent.propTypes = {
  result: PropTypes.object.isRequired,
};

SearchResultItemComponent.defaultProps = {};

export const SearchResultItemLayout = withState(SearchResultItemComponent);
