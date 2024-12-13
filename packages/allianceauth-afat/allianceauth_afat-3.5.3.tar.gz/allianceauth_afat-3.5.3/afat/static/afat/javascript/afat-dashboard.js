/* global afatSettings, characters, moment, manageModal, AFAT_DATETIME_FORMAT */

$(document).ready(() => {
    'use strict';

    /**
     * DataTable :: Recent FATs per character
     */
    if (characters.length > 0) {
        const noFatsWarning = '<div class="aa-callout aa-callout-warning" role="alert">' +
            '<p>' + afatSettings.translation.dataTable.noFatsWarning + ' ###CHARACTER_NAME###</p>' +
            '</div>';

        characters.forEach((character) => {
            $('#recent-fats-character-' + character.charId).DataTable({
                ajax: {
                    url: afatSettings.url.characterFats.replace(
                        '0',
                        character.charId
                    ),
                    dataSrc: '',
                    cache: false
                },
                columns: [
                    {data: 'fleet_name'},
                    {data: 'fleet_type'},
                    {data: 'doctrine'},
                    {data: 'system'},
                    {data: 'ship_type'},
                    {
                        data: 'fleet_time',
                        render: {
                            /**
                             * Render date
                             *
                             * @param data
                             * @returns {*}
                             */
                            display: (data) => {
                                return moment(data.time).utc().format(
                                    AFAT_DATETIME_FORMAT
                                );
                            },
                            _: 'timestamp'
                        }
                    }
                ],
                language: {
                    emptyTable: noFatsWarning.replace(
                        '###CHARACTER_NAME###',
                        character.charName
                    )
                },
                paging: false,
                ordering: false,
                searching: false,
                info: false
            });
        });
    }

    /**
     * DataTable :: Recent FAT links
     */
    const noFatlinksWarning = '<div class="aa-callout aa-callout-warning" role="alert">' +
        '<p>' + afatSettings.translation.dataTable.noFatlinksWarning + '</p>' +
        '</div>';

    const recentFatlinksTableColumns = [
        {data: 'fleet_name'},
        {data: 'fleet_type'},
        {data: 'doctrine'},
        {data: 'creator_name'},
        {
            data: 'fleet_time',
            render: {
                /**
                 * Render timestamp
                 *
                 * @param data
                 * @returns {*}
                 */
                display: (data) => {
                    return moment(data.time).utc().format(AFAT_DATETIME_FORMAT);
                },
                _: 'timestamp'
            }
        }
    ];

    const recentFatlinksTableColumnDefs = [];

    if (afatSettings.permissions.addFatLink === true || afatSettings.permissions.manageAfat === true) {
        recentFatlinksTableColumns.push({
            data: 'actions',
            /**
             * Render action buttons
             *
             * @param data
             * @returns {*|string}
             */
            render: (data) => {
                return data;
            }
        });

        recentFatlinksTableColumnDefs.push({
            targets: [5],
            orderable: false,
            createdCell: (td) => {
                $(td).addClass('text-end');
            }
        });
    }

    $('#dashboard-recent-fatlinks').DataTable({
        ajax: {
            url: afatSettings.url.recentFatLinks,
            dataSrc: '',
            cache: false
        },
        columns: recentFatlinksTableColumns,
        columnDefs: recentFatlinksTableColumnDefs,
        language: {
            emptyTable: noFatlinksWarning
        },
        paging: false,
        ordering: false,
        searching: false,
        info: false
    });

    /**
     * Modal :: Close ESI fleet
     */
    const cancelEsiFleetModal = $(afatSettings.modal.cancelEsiFleetModal.element);
    manageModal(cancelEsiFleetModal);

    /**
     * Modal :: Delete FAT link
     */
    const deleteFatLinkModal = $(afatSettings.modal.deleteFatLinkModal.element);
    manageModal(deleteFatLinkModal);
});
